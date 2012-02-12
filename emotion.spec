#
# Conditional build:
%bcond_without	gstreamer	# don't build gstreamer decoder
%bcond_without	vlc		# don't build vlc generic decoder
%bcond_without	xine		# don't build xine decoder
%bcond_without	static_libs	# don't build static library
#
%define		ecore_ver	1.0.0
%define		edje_ver	1.0.0
%define		eet_ver		1.4.0
%define		eeze_ver	1.1.0
%define		eina_ver	1.0.0
%define		evas_ver	1.0.0

Summary:	Emotion - EFL media playback library
Summary(pl.UTF-8):	Emotion - biblioteka EFL do odtwarzania multimediów
Name:		emotion
Version:	0.2.0.65643
Release:	2
License:	BSD-like
Group:		Libraries
Source0:	http://download.enlightenment.org/snapshots/LATEST/%{name}-%{version}.tar.bz2
# Source0-md5:	1c4fb7c26f4324f4fcc343d6baa21e42
Patch0:		%{name}-am.patch
URL:		http://trac.enlightenment.org/e/wiki/Emotion
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1.6
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	ecore-evas-devel >= %{ecore_ver}
BuildRequires:	ecore-fb-devel >= %{ecore_ver}
BuildRequires:	ecore-x-devel >= %{ecore_ver}
BuildRequires:	edje >= %{edje_ver}
BuildRequires:	edje-devel >= %{edje_ver}
BuildRequires:	eet-devel >= %{eet_ver}
BuildRequires:	eeze-devel >= %{eeze_ver}
BuildRequires:	eio-devel
BuildRequires:	eina-devel >= %{eina_ver}
BuildRequires:	evas-devel >= %{evas_ver}
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 0.10.2
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.34
%endif
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	sed >= 4.0
%{?with_vlc:BuildRequires:	vlc-devel >= 0.9}
%{?with_xine:BuildRequires:	xine-lib-devel >= 2:1.1.1}
Requires:	ecore >= %{ecore_ver}
Requires:	ecore-evas >= %{ecore_ver}
Requires:	ecore-fb >= %{ecore_ver}
Requires:	ecore-x >= %{ecore_ver}
Requires:	edje-libs >= %{edje_ver}
Requires:	eet >= %{eet_ver}
Requires:	eeze >= %{eeze_ver}
Requires:	eina >= %{eina_ver}
Requires:	evas >= %{evas_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emotion is a library to easily integrate media playback into EFL
applications, it will take care of using Ecore's main loop and video
display is done using Evas.

%description -l pl.UTF-8
Emotion to biblioteka pozwalająca na łatwą integrację odtwarzania
multimediów w aplikacjach EFL. Współpracuje z główną pętlą Ecore, a do
wyświetlania wykorzystuje bibliotekę Evas.

%package devel
Summary:	Emotion header files
Summary(pl.UTF-8):	Pliki nagłówkowe Emotion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ecore-devel >= %{ecore_ver}
Requires:	eio-devel
Requires:	eet-devel >= %{eet_ver}
Requires:	eeze-devel >= %{eeze_ver}
Requires:	eina-devel >= %{eina_ver}
Requires:	evas-devel >= %{evas_ver}

%description devel
Header files for Emotion.

%description devel -l pl.UTF-8
Pliki nagłówkowe Emotion.

%package static
Summary:	Static Emotion library
Summary(pl.UTF-8):	Statyczna biblioteka Emotion
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Emotion library.

%description static -l pl.UTF-8
Statyczna biblioteka Emotion.

%package decoder-gstreamer
Summary:	Emotion decoder using gstreamer
Summary(pl.UTF-8):	Dekoder Emotion używający gstreamera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer >= 0.10.2
Requires:	gstreamer-plugins-base >= 0.10.34

%description decoder-gstreamer
Emotion decoder using gstreamer.

%description decoder-gstreamer -l pl.UTF-8
Dekoder Emotion używający gstreamera.

%package decoder-xine
Summary:	Emotion decoder using xine
Summary(pl.UTF-8):	Dekoder Emotion używający xine
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xine-lib >= 2:1.1.1

%description decoder-xine
Emotion decoder using xine.

%description decoder-xine -l pl.UTF-8
Dekoder Emotion używający xine.

%package decoder-vlc
Summary:	Emotion decoder using vlc
Summary(pl.UTF-8):	Dekoder Emotion używający vlc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	vlc >= 0.9

%description decoder-vlc
Emotion decoder using vlc and Emotion generic plugin.

%description decoder-vlc -l pl.UTF-8
Dekoder Emotion używający vlc i wtyczkę generic biblioteki Emotion.

%prep
%setup -q
%patch0 -p1

# fix version for tarball not being svn checkout
%{__sed} -i -e 's/^m4_define.*v_rev.*svnversion.*/m4_define([v_rev], [65643])/' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_vlc:--disable-generic-vlc} \
	%{!?with_gstreamer:--disable-gstreamer} \
	%{!?with_xine:--disable-xine}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/edje/modules/emotion/linux-gnu-*/*.la

%if %{without vlc}
# dir not installed if vlc module not installed
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/utils
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING-PLAIN ChangeLog README TODO
%attr(755,root,root) %{_bindir}/emotion_test
%attr(755,root,root) %{_libdir}/libemotion.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libemotion.so.0
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/em_generic.so
%dir %{_libdir}/%{name}/utils
%dir %{_libdir}/edje/modules/emotion
%dir %{_libdir}/edje/modules/emotion/linux-gnu-*
%attr(755,root,root) %{_libdir}/edje/modules/emotion/linux-gnu-*/module.so
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libemotion.so
%{_libdir}/libemotion.la
%{_includedir}/emotion-0
%{_pkgconfigdir}/emotion.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libemotion.a
%endif

%if %{with gstreamer}
%files decoder-gstreamer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/gstreamer.so
%endif

%if %{with xine}
%files decoder-xine
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/xine.so
%endif

%if %{with vlc}
%files decoder-vlc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/utils/em_generic_vlc
%endif
