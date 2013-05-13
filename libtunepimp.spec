%define major	5
%define libname	%mklibname tunepimp %major
%define libdev	%mklibname tunepimp -d

Name: libtunepimp
Version: 0.5.3
Release: 18
Epoch: 1
Summary: A library for creating MusicBrainz enabled tagging applications
Source0: ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.bz2
Patch0:	tunepimp-0.5.3-build-fix.patch
Patch1:	tunepimp-0.5.3-gcc43.patch
Patch2:	tunepimp-0.5.3-libtool.patch
Patch3: libtunepimp-0.5.3-new-libmp4v2.patch
Patch4:	libtunepimp-0.5.3-gcc44.patch
Patch5: libtunepimp-0.5.3-curl-7.26.patch
Patch6: libtunepimp-automake-1.13.patch
License: GPLv2+
Group: System/Libraries
Url: http://musicbrainz.org/doc/libtunepimp
BuildRequires: pkgconfig(flac)
BuildRequires: readline-devel
BuildRequires: pkgconfig(mad)
BuildRequires: oggvorbis-devel
BuildRequires: pkgconfig(libmusicbrainz)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libofa)
BuildRequires: taglib-devel
BuildRequires: libtool-devel
BuildRequires: libmpcdec-devel
BuildRequires: libmp4v2-devel >= 2.0
BuildRequires: python-devel

%description
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications. 

#-----------------------------------------------------------

%package -n	tunepimp-utils
Summary:	A library for creating MusicBrainz enabled tagging applications
Group:		Sound
Obsoletes:	%{_lib}tunepimp2-utils
Obsoletes:	%{_lib}tunepimp5-utils

%description -n tunepimp-utils
This package contains %{name} tools

%files -n tunepimp-utils
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL README README.LGPL TODO
%{_bindir}/*

#-----------------------------------------------------------

%package -n	tunepimp-plugins
Summary:	A library for creating MusicBrainz enabled tagging applications
Group:		Sound
Obsoletes:	%{_lib}tunepimp2-plugins
Obsoletes:	%{_lib}tunepimp5-plugins

%description -n tunepimp-plugins
This package contains %{name} plugins

%files -n tunepimp-plugins
%defattr(-,root,root)
%dir %{_libdir}/tunepimp/
%dir %{_libdir}/tunepimp/plugins/
%{_libdir}/tunepimp/plugins/flac.tpp
%{_libdir}/tunepimp/plugins/mp3.tpp
%{_libdir}/tunepimp/plugins/mpc.tpp
%{_libdir}/tunepimp/plugins/speex.tpp
%{_libdir}/tunepimp/plugins/tta.tpp
%{_libdir}/tunepimp/plugins/vorbis.tpp
%{_libdir}/tunepimp/plugins/wav.tpp
%{_libdir}/tunepimp/plugins/wma.tpp
%{_libdir}/tunepimp/plugins/wv.tpp

#-----------------------------------------------------------

%package -n	%{libname}
Summary:	A library for creating MusicBrainz enabled tagging applications
Group:		System/Libraries

%description -n	%{libname}
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications.

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

#-----------------------------------------------------------

%package -n	%libdev
Summary:	Files needed for developing applications which use litunepimp
Group:		Development/C
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{libname}
Obsoletes:	%{_lib}tunepimp2-devel
Obsoletes:	%{_lib}tunepimp3-devel
Obsoletes:	%{_lib}tunepimp5-devel

%description -n	%libdev
The %{name}-devel package includes the header files and .so libraries
necessary for developing MusicBrainz enabled tagging applications.

If you are going to develop MusicBrainz enabled tagging 
applications you should install %{name}-devel. You'll also need 
to have the %name package installed.

%files -n %libdev
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

#-----------------------------------------------------------

%package -n	python-tunepimp
Summary:	Python binding to use libtunepimp
Group:		Development/Python
Requires:	python-ctypes
Requires:	%libname = %epoch:%version
%py_requires -d

%description -n python-tunepimp
Python binding to use libtunepimp.

%files -n python-tunepimp
%defattr(-,root,root)
%py_puresitedir/*

#-----------------------------------------------------------

%prep
%setup -q
%apply_patches

# Doesn't build and won't get fixed
sed -i -e 's, mp4,,' plugins/Makefile.am
sed -i -e 's,mp4v2,mp4v3,' configure.in

autoreconf -fi

%build
%configure2_5x \
    --with-included-ltdl=no \
    --with-ltdl-include=%_includedir \
    --with-ltdl-lib=%_libdir \
    --disable-static

%make

%install
%makeinstall_std

cd python
python setup.py install --root=%{buildroot}

# Create symlink for current version includes
cd %buildroot%_includedir
ln -sf tunepimp-0.%major tunepimp


%changelog
* Fri Jun 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:0.5.3-17
+ Revision: 803537
- Make it build in current environment
- Get rid of harmful *.la files

* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.3-16
+ Revision: 686317
- avoid pulling 32 bit libraries on 64 bit arch

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.3-15
+ Revision: 660287
- mass rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.3-14mdv2011.0
+ Revision: 520909
- rebuilt for 2010.1

* Thu Oct 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1:0.5.3-13mdv2010.0
+ Revision: 455890
- rebuild for new curl SSL backend

* Mon Jul 13 2009 Götz Waschk <waschk@mandriva.org> 1:0.5.3-12mdv2010.0
+ Revision: 395453
- replace patch 3 by Gentoo version
- make it build with gcc 4.4

* Sun May 31 2009 Funda Wang <fwang@mandriva.org> 1:0.5.3-11mdv2010.0
+ Revision: 381587
- bump rel
- BR libtool
- build with newer mp4v2

* Mon Jan 12 2009 Götz Waschk <waschk@mandriva.org> 1:0.5.3-10mdv2009.1
+ Revision: 328568
- patch for new libmp4v2
- fix license

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 1:0.5.3-9mdv2009.1
+ Revision: 319698
- rediff gcc 43 patch
- rebuild for new python

* Mon Aug 18 2008 Emmanuel Andry <eandry@mandriva.org> 1:0.5.3-8mdv2009.0
+ Revision: 273392
- fix build with gentoo patches

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Apr 09 2008 Götz Waschk <waschk@mandriva.org> 1:0.5.3-7mdv2009.0
+ Revision: 192444
- build with mp4 metadata support

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1:0.5.3-6mdv2008.1
+ Revision: 150837
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Aug 15 2007 Helio Chissini de Castro <helio@mandriva.com> 1:0.5.3-5mdv2008.0
+ Revision: 63826
- Adde symlink to proper include dir, enable test on apps like kdemultimedia
- Recompile to match new lib name scheme

* Fri Jun 08 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1:0.5.3-3mdv2008.0
+ Revision: 37260
- rebuild for expat
- spec file clean


* Fri Feb 23 2007 Götz Waschk <waschk@mandriva.org> 0.5.3-2mdv2007.0
+ Revision: 124952
- rebuild for new libmpcdec

* Thu Dec 21 2006 Götz Waschk <waschk@mandriva.org> 1:0.5.3-1mdv2007.1
+ Revision: 100984
- readd tta plugin
- new version
- drop patch
- update URL

* Mon Dec 11 2006 Götz Waschk <waschk@mandriva.org> 1:0.5.2-6mdv2007.1
+ Revision: 94981
- patch for new flac

* Tue Nov 28 2006 Götz Waschk <waschk@mandriva.org> 1:0.5.2-4mdv2007.1
+ Revision: 88120
- update file list
- rebuild
- fix directory ownership
- explicitly list all plugins

* Sun Nov 26 2006 Götz Waschk <waschk@mandriva.org> 1:0.5.2-3mdv2007.1
+ Revision: 87329
- optional mp4 build

* Sat Nov 25 2006 Götz Waschk <waschk@mandriva.org> 1:0.5.2-2mdv2007.1
+ Revision: 87221
- fix python dep

* Sat Nov 25 2006 Götz Waschk <waschk@mandriva.org> 1:0.5.2-1mdv2007.1
+ Revision: 87219
- new version
- use correct configure macro
- drop the patch
- add missing python module

* Wed Nov 22 2006 Helio Chissini de Castro <helio@mandriva.com> 1:0.5.1-1mdv2007.1
+ Revision: 86321
- New upstream version
- Removed cve patch ( already applied )

* Thu Nov 09 2006 Laurent Montel <lmontel@mandriva.com> 1:0.4.2-4mdv2007.0
+ Revision: 79967
- Add patch from Gb: fix search plugins in good directory

* Thu Aug 31 2006 Helio Chissini de Castro <helio@mandriva.com> 1:0.4.2-3mdv2007.0
+ Revision: 58886
- Raise release
- Security update:
  http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-3600
  Referenced by http://bugs.musicbrainz.org/ticket/1764

* Wed Aug 09 2006 Helio Chissini de Castro <helio@mandriva.com> 1:0.4.2-2mdv2007.0
+ Revision: 54629
- Right obsoletes

* Fri Aug 04 2006 Helio Chissini de Castro <helio@mandriva.com> 1:0.4.2-1mdv2007.0
+ Revision: 43320
- Add missing source
- Ok, enough with broken libraries. tunepimp 0.5 not work with *any* of included
  programs on distro, and the main one, Amarok, will not include upgrade sooner
  for this version. Reverting for most stable accepted, 0.4.2. In the future we
  need try to be carefull to no upgrade libraries without have sure that all
  affected programs will work.
- import libtunepimp-0.5.0-3mdv2007.0

* Tue Aug 01 2006 Helio Chissini de Castro <helio@mandriva.com> 0.5.0-3mdv2007.0
- Soname is 5 now, no 2. Changing for smooth upgrade.

* Fri Jul 28 2006 Emmanuel Andry <eandry@mandriva.org> 0.5.0-2mdv2007.0
- fix buildrequires

* Wed Jul 26 2006 Emmanuel Andry <eandry@mandriva.org> 0.5.0-1mdv2007.0
- 0.5.0
- builrequires libcurl-devel libofa-devel (created package libofa for this) taglib-devel
- create plugins package

* Sat Nov 26 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.3.0-4mdk
- fix conflict with trm by renaming the example (#19019)

* Tue Apr 19 2005 G�tz Waschk <waschk@mandriva.org> 0.3.0-3mdk
- rebuild for new flac

* Sat Jan 22 2005 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.3.0-2mdk
- rebuild for new readline
- wipe out buildroot at the beginning of %%install
- don't ship the same documents with every package

* Mon Dec 13 2004 Laurent Culioli <laurent@mandrake.org> 0.3.0-1mdk
- initial release.

