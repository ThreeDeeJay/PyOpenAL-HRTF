#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:34:45 2018

@author: Emmanouil Theofanis Chourdakis <e.t.chourdakis@qmul.ac.uk>

An example for hrtf usage adapted from openal-soft's alhrtf.c to PyOpenAL
Original C version by Chris Robinson: https://github.com/kcat/openal-soft/blob/master/examples/alhrtf.c

Original (and current) License:
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.

"""

import argparse
import numpy as np
import time
from openal import *

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('filename', type=str, help='audio filename')
    argparser.add_argument('--hrtf', type=str, help='hrtf name to use (leave out for default)')
    
    args = argparser.parse_args()
    
    if args.hrtf:
        hrtf_name = args.hrtf
    else:
        hrtf_name = None

    # Initialize PyOpenAL
    oalInit()
    
    # Initialize HRTFs
    oalInitHRTF(requested_hrtf=hrtf_name)
    
    # Create a listener at (0,0,0)
    listener = Listener()
    listener.set_position((0,0,0))
    
    # Create a source to play sound with
    source = oalOpen(args.filename)
    
    # Set position of source always relative to the listener
    source.relative = True
    
    # Set position of source
    source.set_position((0., 0., -1.))
    
    # Start playing source until it finishes
    source.play()
    
    angle = 0
    while source.get_state() == al.AL_PLAYING:
        time.sleep(0.01)
        
        # Rotate the source around the lsitener
        # (Taken almost verbatim from alhrtf.c)
        angle += 0.01*np.pi*0.5
        if angle > np.pi:
            angle -= np.pi*2.0
            
        # Update source position
        source.set_position((np.sin(angle), 0., -np.cos(angle)))
        
        # Try to alter stereo angles
        source.set_stereo_angles((np.pi/6.0-angle, -np.pi/6.0-angle))
    
    #Clear up everything
    oalQuit()
