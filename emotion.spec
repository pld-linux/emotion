Summary:	Enlightenment Fundation Libraries - Emotion
Summary(pl):	Podstawowe biblioteki Enlightenmenta - Emotion
Name:		emotion
Version:	0.0.1.004
Release:	1
License:	BSD
Group:		X11/Libraries
Source0:	http://enlightenment.freedesktop.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	3be5850cf23afeff8976e45a9861b7c4
URL:		http://enlightenment.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	edje-devel
BuildRequires:	libtool
BuildRequires:	xine-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emotion is a Media Library.

%description -l pl
Emotion to biblioteka multimedialna.

%package devel
Summary:	Emotion header files
Summary(pl):	Pliki nag³ówkowe Emotion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xine-lib-devel

%description devel
Header files for Emotion.

%description devel -l pl
Pliki nag³ówkowe Emotion.

%package static
Summary:	Static Emotion library
Summary(pl):	Statyczna biblioteka Emotion
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Emotion library.

%description static -l pl
Statyczna biblioteka Emotion.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/xine/plugins/*/*.{la,a} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING-PLAIN README TODO
%attr(755,root,root) %{_bindir}/emotion_*
%attr(755,root,root) %{_libdir}/libemotion.so.*.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/emotion_decoder_xine.so
%{_libdir}/%{name}/emotion_decoder_xine.la
%attr(755,root,root) %{_libdir}/xine/plugins/*/xineplug_vo_out_emotion.so
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/emotion-config
%attr(755,root,root) %{_libdir}/libemotion.so
%{_libdir}/libemotion.la
%{_includedir}/Emotion*
%{_pkgconfigdir}/emotion.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libemotion.a
