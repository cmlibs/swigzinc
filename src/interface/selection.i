/**
 * selection.i
 *
 * Swig interface file for Zinc selection API.
 */
/*
 * Zinc Library
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

%module(package="cmlibs.zinc") selection

%extend CMLibs::Zinc::Selectionnotifier {

    int setCallback(PyObject *callbackObject)
    {
        PyObject *my_callback = NULL;
        if (!PyCallable_Check(callbackObject))
        {
            PyErr_SetString(PyExc_TypeError, "callbackObject must be callable");
            return 0;
        }
        Py_XINCREF(callbackObject);         /* Add a reference to new callback */     /* Remember new callback */
        return cmzn_selectionnotifier_set_callback(($self)->getId(), selectionCallbackToPython, (void *)callbackObject);
    }

    int clearCallback()
    {
      	void *user_data = cmzn_selectionnotifier_get_callback_user_data(($self)->getId());
	    PyObject *callbackObject = static_cast<PyObject *>(user_data);
	    Py_XDECREF(callbackObject);         /* Decrease a reference count */
        return cmzn_selectionnotifier_clear_callback(($self)->getId());
    }
}

%ignore CMLibs::Zinc::Selectionnotifier::clearCallback();

%{
#include "cmlibs/zinc/selection.hpp"

static void selectionCallbackToPython(cmzn_selectionevent_id selectionevent, void *user_data)
{
    PyObject *arglist = NULL;
    PyObject *result = NULL;
    PyObject *my_callback = (PyObject *)user_data;
    /* convert selectionevent to python object */
    PyObject *obj = NULL;
    CMLibs::Zinc::Selectionevent *selectionEvent = new CMLibs::Zinc::Selectionevent(cmzn_selectionevent_access(selectionevent));
    obj = SWIG_NewPointerObj(SWIG_as_voidptr(selectionEvent), SWIGTYPE_p_CMLibs__Zinc__Selectionevent, 1);
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

%include "cmlibs/zinc/selection.hpp"
