#!/usr/bin/env python
import os, glob
from distutils.core import setup
import shutil

VERSION = "0.2.2"
RELEASE = "alpha_1"

if not os.path.exists("mo/"):
    os.mkdir("mo/")
for lang in ('ru', 'uk', 'he'):
    pofile = "po/" + lang + ".po"
    mofile = "mo/" + lang + "/foobnix.mo"
    if not os.path.exists("mo/" + lang + "/"):
        os.mkdir("mo/" + lang + "/")
    print "generating", mofile
    os.system("msgfmt %s -o %s" % (pofile, mofile))


version = file("foobnix/version.py", "wt")
version.write("""
FOOBNIX_VERSION = "%s-%s"
FOOBNIX_RELEASE = "%s"
""" % (VERSION, RELEASE, RELEASE))
version.close()

shutil.copyfile("foobnix.py", "foobnix/foobnix")

setup(name='foobnix',
        version=VERSION,
        description='Foobnix GTK+ music player',
        author='Ivan Ivanenko',
        author_email='ivan.ivanenko@gmail.com',
        url='www.foobnix.com',
        classifiers=[
            'Development Status ::  Beta',
            'Environment :: X11 Applications',
            'Intended Audience :: End Users/Desktop',
            'License :: GNU General Public License (GPL)',
            'Operating System :: Linux',
            'Programming Language :: Python',
            'Topic :: Multimedia :: Sound :: Players',
            ],
         packages=[
                "foobnix",
                "foobnix.base",
                "foobnix.cue",
                "foobnix.dm",
                "foobnix.eq",
                "foobnix.helpers",
                "foobnix.online",
                "foobnix.online.google",
                "foobnix.online.integration",
                "foobnix.preferences",
                "foobnix.preferences.configs",
                "foobnix.radio",
                "foobnix.regui",
                "foobnix.regui.about",
                "foobnix.regui.controls",
                "foobnix.regui.engine",
                "foobnix.regui.id3",
                "foobnix.regui.model",
                "foobnix.regui.notetab",
                "foobnix.regui.service",
                "foobnix.regui.treeview",
                "foobnix.thirdparty",
                "foobnix.thirdparty.google",
                "foobnix.util",
                ],
        scripts=['foobnix/foobnix'],
        data_files=[('share/foobnix', ['README']),
                    ('share/applications', ['foobnix.desktop']),
                    ('share/pixmaps/other', glob.glob('foobnix/pixmaps/other/*')),
                    ('share/pixmaps', glob.glob('foobnix/pixmaps/*.png')),
                    ('share/pixmaps', glob.glob('foobnix/pixmaps/*.jpg')),
                    ('share/pixmaps', glob.glob('foobnix/pixmaps/*.gif')),
                    ('share/pixmaps', glob.glob('foobnix/pixmaps/*.svg')),
                    ('share/foobnix/radio', glob.glob('radio/*')),
                    ('share/man/man1', ['foobnix.1']),
                    ('share/locale/uk/LC_MESSAGES', ['mo/uk/foobnix.mo']),
                    ('share/locale/he/LC_MESSAGES', ['mo/he/foobnix.mo']),
                    ('share/locale/ru/LC_MESSAGES', ['mo/ru/foobnix.mo'])
                    ]
        )

os.remove("foobnix/foobnix")
shutil.rmtree("mo")
shutil.rmtree("build")
