/**
 * region.i
 *
 * Swig interface file for Zinc region API.
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") region

%include "pyzincstringhandling.i"
%typemap(in) (const char *path) = (const char *name);
%typemap(in) (const char *fileName) = (const char *name);

%import "context.i"
%import "fieldmodule.i"
%import "scene.i"
%import "streamregion.i"

%extend CMLibs::Zinc::Region {
	bool operator==(const CMLibs::Zinc::Region& other) const
	{
		return *($self) == other;
	}
}

%extend CMLibs::Zinc::Regionnotifier {

int setCallback(PyObject *callbackObject)
{
    PyObject *my_callback = NULL;
    if (!PyCallable_Check(callbackObject))
    {
        PyErr_SetString(PyExc_TypeError, "callbackObject must be callable");
        return 0;
    }
    Py_XINCREF(callbackObject);         /* Add a reference to new callback */     /* Remember new callback */
    return cmzn_regionnotifier_set_callback(($self)->getId(), regionCallbackToPython, (void *)callbackObject);
}

int clearCallback()
{
    void *user_data = cmzn_regionnotifier_get_callback_user_data(($self)->getId());
    PyObject *callbackObject = static_cast<PyObject *>(user_data);
    Py_XDECREF(callbackObject);         /* Decrease a reference count */
    return cmzn_regionnotifier_clear_callback(($self)->getId());
}
}

%ignore CMLibs::Zinc::Regionnotifier::clearCallback();

%{
#include "cmlibs/zinc/fieldmodule.hpp"
#include "cmlibs/zinc/region.hpp"
#include "cmlibs/zinc/scene.hpp"
#include "cmlibs/zinc/streamregion.hpp"

static void regionCallbackToPython(cmzn_regionevent_id regionevent, void *user_data)
{
    PyObject *arglist = NULL;
    PyObject *result = NULL;
    PyObject *my_callback = (PyObject *)user_data;
    /* convert regionevent to python object */
    PyObject *obj = NULL;
    CMLibs::Zinc::Regionevent *regionEvent = new CMLibs::Zinc::Regionevent(cmzn_regionevent_access(regionevent));
    obj = SWIG_NewPointerObj(SWIG_as_voidptr(regionEvent), SWIGTYPE_p_CMLibs__Zinc__Regionevent, 1);
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

%include "cmlibs/zinc/region.hpp"

