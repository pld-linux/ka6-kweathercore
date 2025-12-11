#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.0
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		kweathercore
Summary:	KWeatherCore
Name:		ka6-%{kaname}
Version:	25.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ba309d89976f27ffac831fbb8f40e079
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kholidays-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
Conflicts:	kde4-libksane >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Get weather forecast and alerts anywhere on the earth easy.
KWeatherCore provides you a highly abstracted library for things
related to weather.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_libdir}/libKWeatherCore.so.*.*
%ghost %{_libdir}/libKWeatherCore.so.6
%dir %{_libdir}/qt6/qml/org/kde/weathercore
%{_libdir}/qt6/qml/org/kde/weathercore/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/weathercore/kweathercoreqmlplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/weathercore/libkweathercoreqmlplugin.so
%{_libdir}/qt6/qml/org/kde/weathercore/qmldir

%files devel
%defattr(644,root,root,755)
%{_includedir}/KWeatherCore
%{_includedir}/kweathercore_version.h
%{_libdir}/cmake/KWeatherCore
%{_libdir}/libKWeatherCore.so
%{_libdir}/qt6/mkspecs/modules/qt_KWeatherCore.pri
