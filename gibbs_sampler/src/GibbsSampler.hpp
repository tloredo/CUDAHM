/*
 * GibbsSampler.hpp
 *
 *  Created on: Jul 25, 2013
 *      Author: Brandon C. Kelly
 */

#ifndef GIBBSSAMPLER_HPP_
#define GIBBSSAMPLER_HPP_

// boost includes
//#include <boost/timer/timer.hpp>
//#include <boost/progress.hpp>

// local includes
#include "parameters.hpp"

class GibbsSampler
{
public:
	// constructor
	GibbsSampler(DataAugmentation& Daug, PopulationPar& PopPar, int niter, int nburnin,
			int nthin_chi=100, int nthin_theta=1);

	// fix the population parameters throughout the sampler?
	void FixPopPar(bool fix=true) { fix_poppar = fix; }
	void FixChar(bool fix=true) { fix_char = fix; }

	// perform a single iterations of the Gibbs Sampler
	virtual void Iterate();

	// run the MCMC sampler
	void Run();

	// print out useful information on the MCMC sampler results
	virtual void Report();

	// save the characteristic samples? not saving them can speed up the sampler since we do not need to
	// read the values from the GPU
	void NoSave(bool nosave = true) {
		if (nosave) {
			Daug_.SetSaveTrace(false);
		} else {
			Daug_.SetSaveTrace(true);
		}
	}

	// grab the MCMC samples
	const vecvec& GetPopSamples() const { return ThetaSamples_; }
	const std::vector<vecvec>& GetCharSamples() const { return ChiSamples_; }
	const std::vector<double>& GetLogDensPop() const { return LogDensPop_Samples_; }
	const std::vector<double>& GetLogDensMeas() const { return LogDensMeas_Samples_; }

protected:
	int niter_, nburnin_, nthin_chi_, nthin_theta_; // total # of iterations, # of burnin iterations, and thinning amount
	int current_iter_, ntheta_samples_, nchi_samples_;
	bool fix_poppar, fix_char; // is set to true, then keep the values fixed throughout the MCMC sampler
	DataAugmentation& Daug_;
	PopulationPar& PopPar_;
	std::vector<vecvec> ChiSamples_;
	vecvec ThetaSamples_;
	std::vector<double> LogDensMeas_Samples_;
	std::vector<double> LogDensPop_Samples_;
};

#endif /* GIBBSSAMPLER_HPP_ */

