#include <algorithm>

#include "mccomposite/geometry/visitors/ArrowIntersector.h"
#include "mccomposite/geometry/visitors/Locator.h"
#include "mccomposite/geometry/intersect.h"
#include "mccomposite/geometry/locate.h"
#include "mccomposite/geometry/shape2ostream.h"
#include "mccomposite/geometry/tolerance.h"

#include "mccomposite/geometry/exception.h"

#include "journal/debug.h"


namespace ArrowIntersector_impl{

  char * jrnltag = "mccomposite.geometry.ArrowIntersector";
  
}


// meta-methods
mccomposite::geometry::ArrowIntersector::ArrowIntersector
()
{
}

mccomposite::geometry::ArrowIntersector::ArrowIntersector
(const arrow_t & arrow)
  : m_arrow( arrow )
{
}

mccomposite::geometry::ArrowIntersector::~ArrowIntersector
()
{
}


// methods
void mccomposite::geometry::ArrowIntersector::setArrow
(const arrow_t & arrow)
{
  m_arrow = arrow;
  reset();
}

void mccomposite::geometry::ArrowIntersector::setArrow
(const Position & start, 
 const Direction & direction)
{
  m_arrow.start = start;
  m_arrow.direction = direction;
  reset();
}


void mccomposite::geometry::ArrowIntersector::reset
()
{
  m_distances.clear();
}

mccomposite::geometry::ArrowIntersector::distances_t
mccomposite::geometry::ArrowIntersector::calculate_intersections
( const AbstractShape & shape ) 
{
  shape.identify( *this );
  return m_distances;
}



#include "mcstas_compact/mcstas_compact.h"

bool isInvaildDirection( const mccomposite::geometry::Direction & direction )
{
  return (direction[0] == 0 && direction[1] == 0 && direction[2] == 0 );
}

// visiting methods
void
mccomposite::geometry::ArrowIntersector::visit
( const Box * boxptr )
{
  m_distances.clear();
  
  const Box & box = *boxptr;
  
  const Position & start = m_arrow.start;
  const Direction & direction = m_arrow.direction;
  if (isInvaildDirection(direction)) return;
  
  double dt_in, dt_out;
  
  double x = start.x; 
  double y = start.y;
  double z = start.z;
  
  double vx = direction.x;
  double vy = direction.y;
  double vz = direction.z;
  
  if ( ! McStas::box_intersect
       ( &dt_in,  &dt_out,  x,  y,  z,  vx,  vy,  vz,  
	 box.edgeX,  box.edgeY,  box.edgeZ) )
    return;
  
  m_distances.push_back( dt_in );
  m_distances.push_back( dt_out );
  
#ifdef DEBUG
  journal::debug_t debug( ArrowIntersector_impl::jrnltag );

  debug << journal::at(__HERE__) 
	<< m_distances << journal::endl
    ;
#endif

  //
  //if (m_distances.size()%2==1) throw Exception("odd number of intersections");
  return ;
}


void
mccomposite::geometry::ArrowIntersector::visit
( const Cylinder * cylptr )
{
  m_distances.clear();
  
  const Cylinder & cylinder = *cylptr;
  
  const Position & start = m_arrow.start;
  const Direction & direction = m_arrow.direction;
  if (isInvaildDirection(direction)) return;
  
  double dt_in, dt_out;
  
  double x = start.x; 
  double y = start.y;
  double z = start.z;
  
  double vx = direction.x;
  double vy = direction.y;
  double vz = direction.z;
  
  if ( ! McStas::cylinder_intersect
       ( &dt_in,  &dt_out,  y,  z,  x,  vy,  vz,  vx,  
	 cylinder.radius, cylinder.height) )
    return;
  
  m_distances.push_back( dt_in );
  m_distances.push_back( dt_out );
  
  //
  //  if (m_distances.size()%2==1) throw Exception("odd number of intersections");
  return;
}




/// calculate intersections of a line through a sphere
/*! the sphere is suppposed to centered in origin
  
  |r| = R
  
  the line is specified by its origin r0 and its direction vector v
  calculation results are specified with t, where t satisfied
  
  r - r0 = t*v
  
  the solution of these two equations is:
  
  t = - ( (r0.v) +/- sqrt( v^2 R^2 - |v X r0|^2 ) ) / v^2
*/
using mccomposite::geometry::Vector;
void calc_intersects_line_sphere
( const Vector & r0, const Vector & v, double R, 
  std::vector<double> & roots )
{
  double r0dotv = (r0|v);
  Vector r0Xv= r0*v;
  double v2 = (v|v);
  
  roots.clear();
  
  double b2m4ac = v2*R*R - (r0Xv|r0Xv);
  
  if (b2m4ac <0) return;
  
//   double acc = 1.e-20;
  
//   if (b2m4ac < acc ) {
//     roots.push_back( - r0dotv/v2);
//     return;
//   }
  
  double sqrt_b2m4ac = sqrt( b2m4ac );
  roots.push_back( - (r0dotv + sqrt_b2m4ac )/v2 );
  roots.push_back( - (r0dotv - sqrt_b2m4ac )/v2 );
  //std::copy( roots.begin(), roots.end(), std::ostream_iterator<double>(std::cout, ",") );
  //std::cout << "\n";
}


void
mccomposite::geometry::ArrowIntersector::visit
( const Sphere * sphereptr )
{
  m_distances.clear();
  
  const Sphere & sphere = *sphereptr;
  
  const Position & start = m_arrow.start;
  const Direction & direction = m_arrow.direction;
  if (isInvaildDirection(direction)) return;
  
  calc_intersects_line_sphere( start, direction, sphere.radius, m_distances );
  //
  //  if (m_distances.size()%2==1) throw Exception("odd number of intersections");
  return;
}



namespace ArrowIntersector_impl{
  
  using namespace mccomposite::geometry;

  struct isNotOnBorder : public std::unary_function<double, bool> {

    isNotOnBorder( const Arrow & arrow, const AbstractShape & shape )
      : m_arrow(arrow), m_shape(shape)
    {}
    bool operator() (double distance) 
    {
      bool ret = locate( m_arrow.start + distance * m_arrow.direction, m_shape ) != Locator::onborder;

#ifdef DEBUG
      journal::debug_t debug( ArrowIntersector_impl::jrnltag );
      
      debug << journal::at(__HERE__) 
	    << "start = " << m_arrow.start << journal::newline
	    << "direction = " << m_arrow.direction << journal::newline
	    << "distance = " << distance << journal::newline
	    << "point = " << m_arrow.start + distance * m_arrow.direction << journal::newline
	    << "shape = " << m_shape << journal::newline
	    << "isNotOnBorder = " << ret
	    << journal::endl;
      ;
#endif
      return ret;
    }
    
  private:
    const Arrow & m_arrow;
    const AbstractShape & m_shape;
  };
  
  
  typedef ArrowIntersector::distances_t distances_t;
  
  // clean up intersection list (distances) so that only 
  // points on border are reserved
  void remove_points_not_on_border
  ( distances_t & dists,
    const Arrow & arrow, const AbstractShape & shape,
    distances_t & ret)
  {
    using namespace std;
    isNotOnBorder isnotonborder( arrow, shape );
    
    remove_copy_if( dists.begin(), dists.end(), back_inserter( ret ),
		    isnotonborder); 
  }

}

namespace mccomposite{ namespace geometry{
    inline bool eq_double( double a, double b ) 
    {
      double max = std::max(std::abs(a), std::abs(b));
      return max < tolerance || std::abs((a-b)/max) < tolerance ;
    }
  }
}

void 
mccomposite::geometry::ArrowIntersector::visit_composition
(const Composition * composition)
{
  const std::vector< const AbstractShape * > & shapes = composition->shapes;
  using namespace ArrowIntersector_impl;

  // gather intersections and remove intersections that are not on border
  distances_t distances;  
  for (size_t i=0; i<shapes.size(); i++) {
    distances_t dists = intersect( m_arrow, *(shapes[i]) );
    remove_points_not_on_border( dists, m_arrow, *composition, distances );
  }
  
  // sort intersections
  std::sort( distances.begin(), distances.end() );

  // this turns out to be more troublesome than not doing it.
  // so let us comment it out:
//   // removed repeated intersection
//   distances_t::iterator newend = std::unique
//     ( distances.begin(), distances.end(), eq_double);

  // copy to result container
  m_distances.clear();
//   copy( distances.begin(), newend, std::back_inserter(m_distances) );
  copy( distances.begin(), distances.end(), std::back_inserter(m_distances) );

#ifdef DEBUG
  journal::debug_t debug( ArrowIntersector_impl::jrnltag );

  debug << journal::at(__HERE__) 
	<< "intersections between " 
	<< "arrow(" << m_arrow.start << "," << m_arrow.direction << ")"
	<< " and shape (" << *composition << ")"
	<< " are "
	<< m_distances << journal::endl
    ;
#endif

  //
  //  if (m_distances.size()%2==1) throw Exception("odd number of intersections");
}


void
mccomposite::geometry::ArrowIntersector::visit
( const Difference * difference ) 
{
  visit_composition( difference );
}

void
mccomposite::geometry::ArrowIntersector::visit
( const Intersection * intersection ) 
{
  visit_composition( intersection );
}

void
mccomposite::geometry::ArrowIntersector::visit
( const Union * aunion ) 
{
  visit_composition( aunion );
}

void
mccomposite::geometry::ArrowIntersector::visit
( const Dilation * dilation ) 
{
  const AbstractShape &body = dilation->body ; 
  const double &scale = dilation->scale ;
  
  Arrow save = m_arrow;
  m_arrow.start = m_arrow.start *(1./scale);
  m_arrow.direction = m_arrow.direction * (1./scale);
  
  body.identify( *this );

#ifdef DEBUG
  journal::debug_t debug( ArrowIntersector_impl::jrnltag );

  debug << journal::at(__HERE__) 
	<< m_distances << journal::endl
    ;
#endif

  m_arrow = save;
  //
  //  if (m_distances.size()%2==1) throw Exception("odd number of intersections");
}


void
mccomposite::geometry::ArrowIntersector::visit
( const Reflection * reflection ) 
{
  throw Exception("not implemented");
}

void
mccomposite::geometry::ArrowIntersector::visit
( const Translation * translation ) 
{
  const AbstractShape &body = translation->body ; 
  const Vector &vector = translation->vector ;

  Arrow save = m_arrow;
  m_arrow.start = m_arrow.start - vector;
  
  body.identify( *this );

  m_arrow = save;
  //
  //  if (m_distances.size()%2==1) throw Exception("odd number of intersections");
}

void
mccomposite::geometry::ArrowIntersector::visit
( const Rotation * rotation )
{
  const AbstractShape &body = rotation->body ; 
  
  RotationMatrix rotmat = rotation->rotmat;

  rotmat.transpose();

  Arrow save = m_arrow;
  m_arrow.start = rotmat * m_arrow.start;
  m_arrow.direction = rotmat * m_arrow.direction;

  body.identify( *this );

  m_arrow = save;
  //
  //  if (m_distances.size()%2==1) throw Exception("odd number of intersections");
}
