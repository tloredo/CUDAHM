/*
 * normnorm.cpp
 *
 *  Created on: Mar 12, 2014
 *      Author: brandonkelly
 */

// std includes
#include <iostream>
#include <fstream>
#include <string>

// local includes
#include "src/kernels.cuh"
#include "src/parameters.cuh"
#include "src/GibbsSampler.hpp"

/*
 * Pointer to the population parameter (theta), stored in constant memory on the GPU. Originally defined in
 * kernels.cu and kernels.cuh. Needed by LogDensityPop, which computes the conditional posterior of the
 * characteristics given the population parameters: log p(chi_i|theta).
 */
extern __constant__ double c_theta[100];

// calculate transpose(x) * covar_inv * x
__device__ __host__
double ChiSqr(double* x, double* covar_inv, int nx)
{
	double chisqr = 0.0;
	for (int i = 0; i < nx; ++i) {
		for (int j = 0; j < nx; ++j) {
			chisqr += x[i] * covar_inv[i * nx + j] * x[j];
		}
	}
	return chisqr;
}

// compute the conditional log-posterior density of the measurements given the characteristic
__device__ __host__
double LogDensityMeas(double* chi, double* meas, double* meas_unc, int mfeat, int pchi)
{
	double logdens = 0.0;
	for (int i = 0; i < pchi; ++i) {
		double chi_std = (meas[i] - chi[i]) / meas_unc[i];
		logdens += -0.5 * chi_std * chi_std;
	}

	return logdens;
}

// compute the conditional log-posterior density of the characteristic given the population mean
__device__ __host__
double LogDensityPop(double* chi, double* theta, int pchi, int dim_theta)
{
	// known inverse covariance matrix of the characteristics
	double covar_inv[9] =
	{
			0.64880351, -2.66823952, 0.10406763,
			-2.66823952, 17.94430089, -0.55439855,
			0.10406763, -0.55439855, 0.02455399
	};
	// subtract off the population mean
	double chi_cent[3];
	for (int i = 0; i < 3; ++i) {
		chi_cent[i] = chi[i] - theta[i];
	}

	double logdens = -0.5 * ChiSqr(chi_cent, covar_inv, 3);
	return logdens;
}

/*
 * Pointers to the device-side functions used to compute the conditional log-densities. These must be defined by the user, as
 * illustrated below.
 */
__constant__ pLogDensMeas c_LogDensMeas = LogDensityMeas;  // log p(y_i|chi_i)
__constant__ pLogDensPop c_LogDensPop = LogDensityPop;  // log p(chi_i|theta)

// return the number of lines in a text file
int get_file_lines(std::string& filename) {
    int number_of_lines = 0;
    std::string line;
    std::ifstream inputfile(filename.c_str());

    while (std::getline(inputfile, line))
        ++number_of_lines;
    inputfile.close();
    return number_of_lines;
}

// read in the data
void read_data(std::string& filename, double** meas, double** meas_unc, int ndata, int mfeat) {
	std::ifstream input_file(filename.c_str());
	for (int i = 0; i < ndata; ++i) {
		for (int j = 0; j < mfeat; ++j) {
			input_file >> meas[i][j] >> meas_unc[i][j];
		}
	}
	input_file.close();
}

// dump the sampled values of the population parameter to a text file
void write_thetas(std::string& filename, vecvec& theta_samples) {
	std::ofstream outfile(filename.c_str());
	int nsamples = theta_samples.size();
	int dtheta = theta_samples[0].size();
	for (int i = 0; i < nsamples; ++i) {
		for (int j = 0; j < dtheta; ++j) {
			outfile << theta_samples[i][j];
		}
		outfile << std::endl;
	}
}

// dump the posterior means and standard deviations of the characteristics to a text file
void write_chis(std::string& filename, std::vector<vecvec>& chi_samples) {
	std::ofstream outfile(filename.c_str());
	int nsamples = chi_samples.size();
	int ndata = chi_samples[0].size();
	int pchi = chi_samples[0][0].size();

	for (int i = 0; i < ndata; ++i) {
		std::vector<double> post_mean_i(pchi, 0.0);
		std::vector<double> post_msqr_i(pchi, 0.0);  // posterior mean of the square of the values for chi_i
		for (int j = 0; j < nsamples; ++j) {
			for (int k = 0; k < pchi; ++k) {
				post_mean_i[k] += chi_samples[j][i][k] / nsamples;
				post_msqr_i[k] += chi_samples[j][i][k] * chi_samples[j][i][k] / nsamples;
			}
		}
		for (int k = 0; k < pchi; ++k) {
			double post_sigma_ik = sqrt(post_msqr_i[k] - post_mean_i[k] * post_mean_i[k]);  // posterior standard deviation
			outfile << post_mean_i[k] << " " << post_sigma_ik;
		}
		outfile << std::endl;
	}

	outfile.close();
}

int main(int argc, char** argv)
{
	// known dimensions of features, characteristics and population parameter
	const int mfeat = 3;
	const int pchi = 3;
	const int dtheta = 3;

	// allocate memory for measurement arrays
	double** meas;
	double** meas_unc;
	std::string filename("normnorm_example.dat");
	int ndata = get_file_lines(filename);

    meas = new double* [ndata];
    meas_unc = new double* [ndata];
    for (int i = 0; i < ndata; ++i) {
		meas[i] = new double [mfeat];
		meas_unc[i] = new double [mfeat];
	}

    // read in measurement data from text file
    read_data(filename, meas, meas_unc, ndata, mfeat);

	// Cuda grid launch, TODO: should move this to within the GibbsSampler constructor
    dim3 nThreads(256);
    dim3 nBlocks((ndata + nThreads.x-1) / nThreads.x);
    printf("nBlocks: %d\n", nBlocks.x);  // no more than 64k blocks!
    if (nBlocks.x > 65535)
    {
        std::cerr << "ERROR: Block is too large" << std::endl;
        return 2;
    }

    // build the MCMC sampler
    int niter = 50000;
    int nburnin = niter / 2;

    int nchi_samples = 1000;  // only keep 100 samples for the chi values since we have so many of them
    int nthin_chi = niter / nchi_samples;

    GibbsSampler<mfeat, pchi, dtheta> Sampler(meas, meas_unc, ndata, nBlocks, nThreads, niter, nburnin, nthin_chi);

    // launch the MCMC sampler
    Sampler.Run();

    // grab the samples
    vecvec theta_samples = Sampler.GetPopSamples();  // vecvec is a typedef for std::vector<std::vector<double> >
    std::vector<vecvec> chi_samples = Sampler.GetCharSamples();

    std::cout << "Writing results to text files..." << std::endl;

    // write the sampled theta values to a file. output will have nsamples rows and dtheta columns.
    std::string thetafile("normnorm_thetas.dat");
    write_thetas(thetafile, theta_samples);

    // write the posterior means and standard deviations of the characteristics to a file. output will have ndata rows and
    // 2 * pchi columns, where the columns format is posterior mean 1, posterior sigma 1, posterior mean 2, posterior sigma 2, etc.
    std::string chifile("normnorm_chi_summary.dat");
    write_chis(chifile, chi_samples);

	// free memory
	for (int i = 0; i < ndata; ++i) {
		delete [] meas[i];
		delete [] meas_unc[i];
	}
	delete meas;
	delete meas_unc;
}
