/**
 * stream.i
 *
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") stream

%include "pyzincstringhandling.i"
%typemap(in) (const char *file_name) = (const char *name);

%{
#include "cmlibs/zinc/stream.hpp"
#include "cmlibs/zinc/streamimage.hpp"
#include "cmlibs/zinc/streamregion.hpp"
#include "cmlibs/zinc/streamscene.hpp"
%}

%extend CMLibs::Zinc::Streaminformation {
	CMLibs::Zinc::StreamresourceMemory createStreamresourceMemoryBuffer(const void *buffer, unsigned int buffer_length)
	{
		return $self->createStreamresourceMemoryBufferCopy(buffer, buffer_length);
	}
}

%ignore CMLibs::Zinc::Streaminformation::createStreamresourceMemoryBuffer(const void *buffer, unsigned int buffer_length);

%include "cmlibs/zinc/stream.hpp"
