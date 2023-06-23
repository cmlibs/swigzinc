/**
 * scenefilter.i
 *
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") scenefilter

%include "pyzincstringhandling.i"
%typemap(in) (const char *matchName) = (const char *name);

%import "graphics.i"
%import "region.i"

%extend CMLibs::Zinc::Scenefilter {
	bool operator==(const CMLibs::Zinc::Scenefilter& other) const
	{
		return *($self) == other;
	}
}

%{
#include "cmlibs/zinc/scenefilter.hpp"
#include "cmlibs/zinc/fieldconditional.hpp"
%}

%include "cmlibs/zinc/scenefilter.hpp"

