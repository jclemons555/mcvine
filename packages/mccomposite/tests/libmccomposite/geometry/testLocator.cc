// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                         (C) 2005 All Rights Reserved  
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#include <cassert>
#include <iostream>
#include "mccomposite/geometry/shapes.h"
#include "mccomposite/geometry/locate.h"


using namespace mccomposite::geometry;

void test1()
{
  Box box(1,2,3);
  Locator locator;
  locator.setPoint( Position(0,0,0) );
  assert (locator.locate( box ) == Locator::inside);
}

void test1a()
{
  Cylinder cylinder(1,2);
  assert (locate( Position(0,0,0), cylinder ) == Locator::inside);
  assert (locate( Position(0,0,1), cylinder ) == Locator::onborder);
  assert (locate( Position(0,0,1.01), cylinder ) == Locator::outside);
  assert (locate( Position(0,1,0), cylinder ) == Locator::onborder);
  assert (locate( Position(0,1.01,0), cylinder ) == Locator::outside);
  assert (locate( Position(1,0,0), cylinder ) == Locator::onborder);
  assert (locate( Position(1.01,0,0), cylinder ) == Locator::outside);
  assert (locate( Position(0.708,0.708,0), cylinder ) == Locator::outside);
  assert (locate( Position(1,0,1), cylinder ) == Locator::onborder);
  assert (locate( Position(-1,0,1), cylinder ) == Locator::onborder);
  assert (locate( Position(1,0,-1), cylinder ) == Locator::onborder);
  assert (locate( Position(-1,0,-1), cylinder ) == Locator::onborder);
}

void test1b()
{
  Sphere sphere(1);
  assert (locate( Position(0,0,0), sphere ) == Locator::inside);
  assert (locate( Position(1,0,0), sphere ) == Locator::onborder);
  assert (locate( Position(-1,0,0), sphere ) == Locator::onborder);
  assert (locate( Position(0,1,0), sphere ) == Locator::onborder);
  assert (locate( Position(0,-1,0), sphere ) == Locator::onborder);
  assert (locate( Position(0,0,1), sphere ) == Locator::onborder);
  assert (locate( Position(0,0,-1), sphere ) == Locator::onborder);
  assert (locate( Position(0.707,0.707,0), sphere ) == Locator::inside);
  assert (locate( Position(0.708,0.708,0), sphere ) == Locator::outside);
  assert (locate( Position(-0.707,0.707,0), sphere ) == Locator::inside);
  assert (locate( Position(-0.708,0.708,0), sphere ) == Locator::outside);
  assert (locate( Position(0.707,0,0.707), sphere ) == Locator::inside);
  assert (locate( Position(0.708,0,0.708), sphere ) == Locator::outside);
  assert (locate( Position(0.707,0,-0.707), sphere ) == Locator::inside);
  assert (locate( Position(0.708,0,-0.708), sphere ) == Locator::outside);
}

void test1c()
{
  Pyramid pyramid(2,3, 5);
  // center of base
  assert (locate( Position(0,0,-5), pyramid ) == Locator::onborder);
  // inside, along axis
  assert (locate( Position(0,0,1-5), pyramid ) == Locator::inside);
  assert (locate( Position(0,0,2-5), pyramid ) == Locator::inside);
  assert (locate( Position(0,0,4.99-5), pyramid ) == Locator::inside);
  // outside, along axis
  assert (locate( Position(0,0,5.01-5), pyramid ) == Locator::outside);
  // base, corner
  assert (locate( Position(1,1.5,0-5), pyramid ) == Locator::onborder);
  // inside, near base, near corner
  assert (locate( Position(1-0.02,1.5-0.02,0+0.01-5), pyramid ) == Locator::inside);
  // inside, near base, near edge
  assert (locate( Position(1-0.02,0,0+0.01-5), pyramid ) == Locator::inside);
  // inside, near base, near another corner
  assert (locate( Position(1-0.02,-1.5+0.02,0+0.01-5), pyramid ) == Locator::inside);
  // inside, near base, near another corner
  assert (locate( Position(-1+0.02,-1.5+0.02,0+0.01-5), pyramid ) == Locator::inside);
  // outside, near base, near corner
  assert (locate( Position(1+0.02,1.5+0.02,0+0.01-5), pyramid ) == Locator::outside);
  // outside, near base, near edge
  assert (locate( Position(1+0.02,0,0+0.01-5), pyramid ) == Locator::outside);
  // outside, near base, near another corner
  assert (locate( Position(1+0.02,-1.5+0.02,0+0.01-5), pyramid ) == Locator::outside);
  // outside, near base, near another corner
  assert (locate( Position(-1+0.02,-1.5-0.02,0+0.01-5), pyramid ) == Locator::outside);
  // base, on border, near a corner
  assert (locate( Position(-1,-1.5,0-5), pyramid ) == Locator::onborder);
  // outside, near tip
  assert (locate( Position(.2,.2,5-5), pyramid ) == Locator::outside);
  // inside, near tip
  assert (locate( Position(0,0,5-0.01-5), pyramid ) == Locator::inside);
  // border, tip
  assert (locate( Position(0,0,5-5), pyramid ) == Locator::onborder);
  // inside, half hight, near corner
  assert (locate( Position(.5-0.02,.75-0.02,2.5-5), pyramid ) == Locator::inside);
  // inside, half hight, near edge
  assert (locate( Position(.5-0.02,0,2.5-5), pyramid ) == Locator::inside);
  // inside, half hight, near another corner
  assert (locate( Position(.5-0.02,-.75+0.02,2.5-5), pyramid ) == Locator::inside);
  // inside, half hight, near another corner
  assert (locate( Position(-.5+0.02,-.75+0.02,2.5-5), pyramid ) == Locator::inside);
  // outside, half hight, near corner
  assert (locate( Position(.5+0.02,.75+0.02,2.5-5), pyramid ) == Locator::outside);
  // outside, half hight, near edge
  assert (locate( Position(.5+0.02,0,2.5-5), pyramid ) == Locator::outside);
  // outside, half hight, near another corner
  assert (locate( Position(.5+0.02,-.75+0.02,2.5-5), pyramid ) == Locator::outside);
  // outside, half hight, near another corner
  assert (locate( Position(-.5+0.02,-.75-0.02,2.5-5), pyramid ) == Locator::outside);
  // onborder, half hight, near corner
  assert (locate( Position(.5,.75,2.5-5), pyramid ) == Locator::onborder);
  // onborder, half hight, near edge
  assert (locate( Position(.5,0,2.5-5), pyramid ) == Locator::onborder);
  // onborder, half hight, near another corner
  assert (locate( Position(.5,-.75,2.5-5), pyramid ) == Locator::onborder);
  // onborder, half hight, near another corner
  assert (locate( Position(-.5,-.75,2.5-5), pyramid ) == Locator::onborder);
}

void test2()
{
  Box box(1,1,1);
  assert (locate( Position(0,0,0), box ) == Locator::inside);
  assert (locate( Position(0,0,0.51), box ) == Locator::outside);
  assert (locate( Position(0,0,0.5), box ) == Locator::onborder);
}

void test3()
{
  Box box1(1,1,1);
  Box box2(2,2,2);
  Difference diff(box2, box1);
  assert (locate( Position(0,0,0), diff ) == Locator::outside);
  assert (locate( Position(0,0,0.51), diff ) == Locator::inside);
  assert (locate( Position(0,0,0.5), diff ) == Locator::onborder);
}

void test4()
{
  Box box(1,1,1);
  Translation translation(box, Vector(0,0,0.5));

  Intersection intersection(box, translation);

  assert (locate( Position(0,0,0), intersection ) == Locator::onborder);
  assert (locate( Position(0,0,0.51), intersection ) == Locator::outside);
  assert (locate( Position(0,0,0.2), intersection ) == Locator::inside);

  Box box1(2,2,2);
  Intersection intersection2(box1, translation);
  assert (locate( Position(0,0,1), intersection2 ) == Locator::onborder);
  assert (locate( Position(0,0,0), intersection2 ) == Locator::onborder);

  Cylinder cylinder(2,2);
  Sphere sphere(2);
  Intersection intersection3(cylinder, sphere);
  assert (locate( Position(0,0,1), intersection3 ) == Locator::onborder);
  assert (locate( Position(0,0,2), intersection3 ) == Locator::outside);

}

void test5()
{
  Box box(1,1,1);
  Translation translation(box, Vector(0,0,0.5));

  Union aunion(box, translation);

  assert (locate( Position(0,0,0), aunion ) == Locator::inside);
  assert (locate( Position(0,0,1.01), aunion ) == Locator::outside);
  assert (locate( Position(0,0,1.00), aunion ) == Locator::onborder);
}

void test6()
{
  Box box(1,1,1);
  Dilation dilation(box, 5);

  assert (locate( Position(0,0,0), dilation ) == Locator::inside);
  assert (locate( Position(0,0,2.51), dilation ) == Locator::outside);
  assert (locate( Position(0,0,2.50), dilation ) == Locator::onborder);
}

void test7()
{
  Box box(1,1,10);
  RotationMatrix m(1,0,0,
		   0,0,1,
		   0,-1,0);
  Rotation rotated(box, m);

  assert (locate( Position(0,0,0), rotated ) == Locator::inside);
  assert (locate( Position(0,5.001, 0), rotated ) == Locator::outside);
  assert (locate( Position(0,5.0, 0), rotated ) == Locator::onborder);
}

int main()
{
  test1();
  test1a();
  test1b();
  test1c();
  test2();
  test3();
  test4();
  test5();
  test6();
  test7();
}

// version
// $Id$

// End of file 
