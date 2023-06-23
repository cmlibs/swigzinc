/**
 * streamimage.i
 *
 * Swig interface file for Zinc image stream API.
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") streamimage

%include "pyzincstringhandling.i"

%import "stream.i"

%{
#include "cmlibs/zinc/streamimage.hpp"
%}

%include "cmlibs/zinc/streamimage.hpp"
