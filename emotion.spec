#
# Conditional build:
%bcond_without	gstreamer	# don't build gstreamer decoder
%bcond_without	xine		# don't build xine decoder
%bcond_without	static_libs	# don't build static library
#
%if !%{with gstreamer} && !%{with xine}
%error at last one backend must be enabled
%endif
#
%define		ecore_ver	0.9.9.043
%define		edje_ver	0.9.9.043
%define		evas_ver	0.9.9.043

Summary:	Enlightenment Fundation Libraries - Emotion
Summary(pl.UTF-8):	Podstawowe biblioteki Enlightenmenta - Emotion
Name:		emotion
Version:	0.1.0.042
Release:	1
License:	BSD
Group:		X11/Libraries
Source0:	http://download.enlightenment.org/snapshots/2008-01-25/%{name}-%{version}.tar.bz2
# Source0-md5:	123c043d02f4da22fb36eede930a44e5
URL:		http://enlightenment.org/p.php?p=about/libs/emotion
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
# ecore-evas ecore-job
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	edje >= %{edje_ver}
BuildRequires:	edje-devel >= %{edje_ver}
BuildRequires:	evas-devel >= %{evas_ver}
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 0.10.2
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.1
# gstreamer-cdio,gstreamer-ffmpeg for runtime, configure just warns if missing
%endif
BuildRequires:	libtool
BuildRequires:	pkgconfig
%{?with_xine:BuildRequires:	xine-lib-devel >= 2:1.1.1}
Requires:	ecore-evas >= %{ecore_ver}
Requires:	ecore-job >= %{ecore_ver}
Requires:	edje-libs >= %{edje_ver}
Requires:	evas >= %{evas_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emotion is a Media Library.

%description -l pl.UTF-8
Emotion to biblioteka multimedialna.

%package devel
Summary:	Emotion header files
Summary(pl.UTF-8):	Pliki nagłówkowe Emotion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# ecore-evas ecore-job
Requires:	ecore-devel >= %{ecore_ver}
Requires:	edje-devel >= %{edje_ver}
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
Requires:	gstreamer-plugins-base >= 0.10.1
Suggests:	gstreamer-cdio
Suggests:	gstreamer-ffmpeg

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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{!?with_gstreamer:--disable-gstreamer} \
	%{!?with_xine:--disable-xine}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING-PLAIN README TODO
%attr(755,root,root) %{_bindir}/emotion_*
%attr(755,root,root) %{_libdir}/libemotion.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libemotion.so.0
%dir %{_libdir}/%{name}
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libemotion.so
%{_libdir}/libemotion.la
%{_includedir}/Emotion.h
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
