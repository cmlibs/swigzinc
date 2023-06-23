/**
 * tessellation.i
 *
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") tessellation

%extend CMLibs::Zinc::Tessellationmodulenotifier {

	int setCallback(PyObject *callbackObject)
	{
		PyObject *my_callback = NULL;
		if (!PyCallable_Check(callbackObject))
		{
			PyErr_SetString(PyExc_TypeError, "callbackObject must be callable");
			return 0;
		}
		Py_XINCREF(callbackObject);         /* Add a reference to new callback */     /* Remember new callback */
		return cmzn_tessellationmodulenotifier_set_callback(($self)->getId(), tessellationmoduleCallbackToPython, (void *)callbackObject);
	}

	int clearCallback()
	{
		void *user_data = cmzn_tessellationmodulenotifier_get_callback_user_data(($self)->getId());
		PyObject *callbackObject = static_cast<PyObject *>(user_data);
		Py_XDECREF(callbackObject);         /* Decrease a reference count */
		return cmzn_tessellationmodulenotifier_clear_callback(($self)->getId());
	}
}

%ignore CMLibs::Zinc::Tessellationmodulenotifier::clearCallback();

%include "integervaluesarraytypemap.i"
%include "pyzincstringhandling.i"

%extend CMLibs::Zinc::Tessellation {
	bool operator==(const CMLibs::Zinc::Tessellation& other) const
	{
		return *($self) == other;
	}
}

%{
#include "cmlibs/zinc/tessellation.hpp"

static void tessellationmoduleCallbackToPython(cmzn_tessellationmoduleevent_id tessellationmoduleevent, 
	void *user_data)
{
	PyObject *arglist = NULL;
	PyObject *result = NULL;
	PyObject *my_callback = (PyObject *)user_data;
	/* convert tessellationmoduleevent to python object */
	PyObject *obj = NULL;
	CMLibs::Zinc::Tessellationmoduleevent *tessellationmoduleEvent = 
		new CMLibs::Zinc::Tessellationmoduleevent(cmzn_tessellationmoduleevent_access(tessellationmoduleevent));
	obj = SWIG_NewPointerObj(SWIG_as_voidptr(tessellationmoduleEvent), SWIGTYPE_p_CMLibs__Zinc__Tessellationmoduleevent, 1);
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

%include "cmlibs/zinc/tessellation.hpp"
