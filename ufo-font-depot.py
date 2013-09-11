#!/usr/bin/python
# -*- coding: utf-8 -*-
# ufo-font-generator.py
# Copyright (c) 2013, Dave Crossland (dave@understandingfonts.com)
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
#   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#   EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""A FontForge plug-in to automatically generate UFO fonts.

Copy to ~/.FontForge/python/ and then find "Generate UFO" in the Tools menu 
(run it by pressing §) and "Reload UFO" (press Shift+§)"""

import os, sys

def activateFont(fontOrGlyph):
    """
    Return the active font, given an object that could be either a font or glyph
    """
    if getattr(fontOrGlyph, 'font', None):
        font = fontOrGlyph.font
    else:
        font = fontforge.activeFont()
    if font.path[:1] == '/':
        fontPath = font.path[:-1]
    else:
        fontPath = font.path
    path, filename = os.path.split(fontPath) # split the path
    filenameStem, extension = os.path.splitext(filename) # split the filename
    ufo = os.path.join(path + os.sep + filenameStem + '.ufo')
    return font, ufo

def generateUfo(registerObject, fontOrGlyph):
    """
    Generate a UFO from the currently active font, using the PS Name as the filename
    """
    font, ufo = activateFont(fontOrGlyph)
    font.generate(ufo)
    msg = "Generated UFO: " + ufo
    fontforge.logWarning(msg)

def reloadUfo(registerObject, fontOrGlyph):
    """
    Generate a UFO from the currently active font, using the PS Name as the filename
    """
    font, ufo = activateFont(fontOrGlyph)
    font.revert()
    msg = "Reloaded UFO: " + ufo
    fontforge.logWarning(msg)

def enableFunction(registerObject, fontOrGlyph):
    """
    Enable if the font has been named (in Font Info)
    """
    font, ufo = activateFont(fontOrGlyph)
    # if the first 8 chars in the PS Name are 'Untitled'
    if font.fontname[0:8] == "Untitled":
        return False
    else:
        return True

# Hook this into the Tools menu of both Font and Glyph windows
if fontforge.hasUserInterface():
    # generateUfo()
    registerObject = None
    windowsToAppearIn = ("Font","Glyph")
    keyShortcut="§" # Could be "Ctrl-§", or anything not set in hotkeys file
    menuText = "Generate UFO"
    fontforge.registerMenuItem(generateUfo,enableFunction,registerObject,windowsToAppearIn,keyShortcut,menuText)
    # reloadUfo()
    registerObject = None
    windowsToAppearIn = ("Font","Glyph")
    keyShortcut="Shft+§" # Could be "Ctrl-§", or anything not set in hotkeys file
    menuText = "Reload UFO"
    fontforge.registerMenuItem(reloadUfo,enableFunction,registerObject,windowsToAppearIn,keyShortcut,menuText)
