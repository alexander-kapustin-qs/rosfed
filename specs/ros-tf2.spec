Name:           ros-tf2
Version:        noetic.0.7.5
Release:        3%{?dist}
Summary:        ROS package tf2

License:        BSD
URL:            http://www.ros.org/wiki/tf2

Source0:        https://github.com/ros-gbp/geometry2-release/archive/release/noetic/tf2/0.7.5-1.tar.gz#/ros-noetic-tf2-0.7.5-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cpp_common-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel
BuildRequires:  ros-noetic-roscpp_traits-devel
BuildRequires:  ros-noetic-rostime-devel
BuildRequires:  ros-noetic-tf2_msgs-devel

Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-rostime
Requires:       ros-noetic-tf2_msgs

Provides:  ros-noetic-tf2 = 0.7.5-3
Obsoletes: ros-noetic-tf2 < 0.7.5-3
Obsoletes: ros-kinetic-tf2 < 0.7.5-3



%description
tf2 is the second generation of the transform library, which lets the
user keep track of multiple coordinate frames over time. tf2 maintains
the relationship between coordinate frames in a tree structure
buffered in time, and lets the user transform points, vectors, etc
between any two coordinate frames at any desired point in time.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       gtest-devel
Requires:       ros-noetic-cpp_common-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-roscpp_serialization-devel
Requires:       ros-noetic-roscpp_traits-devel
Requires:       ros-noetic-rostime-devel
Requires:       ros-noetic-tf2_msgs-devel

Provides: ros-noetic-tf2-devel = 0.7.5-3
Obsoletes: ros-noetic-tf2-devel < 0.7.5-3
Obsoletes: ros-kinetic-tf2-devel < 0.7.5-3


%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install

PYTHONUNBUFFERED=1 ; export PYTHONUNBUFFERED

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \

source %{_libdir}/ros/setup.bash

# substitute shebang before install block because we run the local catkin script
%py3_shebang_fix .

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg tf2




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/tf2/cmake} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@.*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list

%py3_shebang_fix %{buildroot}

# Also fix .py.in files
for pyfile in $(grep -rIl '^#!.*python.*$' %{buildroot}) ; do
  %py3_shebang_fix $pyfile
done


%files -f files.list
%files devel -f files_devel.list


%changelog
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.7.5-3
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.7.5-2
- Modernize python shebang replacement
* Thu Sep 10 2020 Nicolas Limpert <limpert@fh-aachen.de> - noetic.0.7.5-1
- Update to latest release
* Sat Aug 08 2020 Nicolas Limpert - noetic.0.7.2-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.7.1-2
- Remove upstreamed patch
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.7.1-1
- Upgrade to noetic
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.6.5-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.6.5-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.6.5-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.5.20-2
- Remove ROS distro from package name
* Thu Mar 14 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.5.20-1
- Update to latest release
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.19-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-9
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-8
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-7
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-6
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-5
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-4
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-3
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-2
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.17-1
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.16-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.16-1
- Update auto-generated Spec file
