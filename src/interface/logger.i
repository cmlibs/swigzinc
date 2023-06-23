/**
 * logger.i
 *
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") logger

%extend CMLibs::Zinc::Loggernotifier {

	int setCallback(PyObject *callbackObject)
	{
		PyObject *my_callback = NULL;
		if (!PyCallable_Check(callbackObject))
		{
			PyErr_SetString(PyExc_TypeError, "callbackObject must be callable");
			return 0;
		}
		Py_XINCREF(callbackObject);         /* Add a reference to new callback */     /* Remember new callback */
		return cmzn_loggernotifier_set_callback(($self)->getId(), loggerCallbackToPython, (void *)callbackObject);
	}

	int clearCallback()
	{
		void *user_data = cmzn_loggernotifier_get_callback_user_data(($self)->getId());
		PyObject *callbackObject = static_cast<PyObject *>(user_data);
		Py_XDECREF(callbackObject);         /* Decrease a reference count */
		return cmzn_loggernotifier_clear_callback(($self)->getId());
	}
}

%ignore CMLibs::Zinc::Loggernotifier::clearCallback();

%include "integervaluesarraytypemap.i"
%include "pyzincstringhandling.i"

%extend CMLibs::Zinc::Logger {
	bool operator==(const CMLibs::Zinc::Logger& other) const
	{
		return *($self) == other;
	}
}

%{
#include "cmlibs/zinc/core.h"
#include "cmlibs/zinc/logger.hpp"

static void loggerCallbackToPython(cmzn_loggerevent_id loggerevent, 
	void *user_data)
{
	PyObject *arglist = NULL;
	PyObject *result = NULL;
	PyObject *my_callback = (PyObject *)user_data;
	/* convert loggerevent to python object */
	PyObject *obj = NULL;
	CMLibs::Zinc::Loggerevent *loggerEvent = 
		new CMLibs::Zinc::Loggerevent(cmzn_loggerevent_access(loggerevent));
	obj = SWIG_NewPointerObj(SWIG_as_voidptr(loggerEvent), SWIGTYPE_p_CMLibs__Zinc__Loggerevent, 1);
	/* Time to call the callback */
	arglist = Py_BuildValue("(N)", obj);
	result = PyObject_CallObject(my_callback, arglist);
	Py_DECREF(arglist);
	if (result)
	{
		Py_DECREF(result);
	}
}
%}

%include "cmlibs/zinc/logger.hpp"
