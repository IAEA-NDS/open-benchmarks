#include <memory> // for unique_ptr

#include "openmc/random_lcg.h"
#include "openmc/random_dist.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/geometry.h"
#include "openmc/cell.h"

class CompiledSource : public openmc::Source
{
  openmc::SourceSite sample(uint64_t* seed) const
  {
    
    openmc::SourceSite particle;
    particle.particle = openmc::ParticleType::neutron;
    particle.wgt = 0.0;
    int i = 0;
    int efficiency = 100000;
    // position
    while (i < efficiency) {
      particle.r.x = openmc::uniform_distribution(-1115.2, 1115.2, seed);
      particle.r.y = openmc::uniform_distribution(-1115.2, 1115.2, seed);
      particle.r.z = openmc::uniform_distribution(-1000.2, 1000.2, seed);
      // check position
      bool accepted = check_cell(particle.r);
      if (accepted) {
        particle.wgt = 1.0;
        i = efficiency;
      }
      i++;
    }
    // angle
    double theta = openmc::uniform_distribution(0.0, 2*M_PI, seed);
    double phi = std::acos(openmc::uniform_distribution(-1.0, 1.0, seed));
    double ux = std::sin(phi)*std::cos(theta);
    double uy = std::sin(phi)*std::sin(theta);
    double uz = std::cos(phi);
    particle.u = {ux, uy, uz};
    // energy
    double mean = 14.055843863040961e6; 
    double stdev = 0.23863574091114037e6;
    particle.E = openmc::normal_variate(mean, stdev, seed);
    particle.delayed_group = 0;
    return particle;
  }
  bool check_cell(openmc::Position r) const
  {
    openmc::GeometryState geom_state;
    geom_state.r() = r;
    geom_state.u() = {0.0, 0.0, 1.0};
    // Reject particle if it's not in the geometry at all
    bool found = exhaustive_find_cell(geom_state);
    if (!found)
        return false;
    // Check if particle is in cell 51
    int domain_id = 51;
    for (int i = 0; i < geom_state.n_coord(); i++) {
      int id = openmc::model::cells[geom_state.coord(i).cell()].get()->id_;
      if (domain_id != id) {
        return false;
      } 
      else {
        return true;
      }   
    }
    return 0;
  }
};

extern "C" std::unique_ptr<CompiledSource> openmc_create_source(std::string parameters)
{
  return std::make_unique<CompiledSource>();
}