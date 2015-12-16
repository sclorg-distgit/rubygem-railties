%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from railties-3.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name railties

%global download_path http://rubygems.org/downloads/


%global runtests 1

Summary: Tools for creating, working with, and running Rails applications
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 4.1.5
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: %{download_path}%{gem_name}-%{version}.gem
# ** Take LICENSE file from upstream. **
# wget --no-check-certificate https://github.com/rails/rails/raw/master/railties/MIT-LICENSE
Source1: http://github.com/rails/rails/raw/master/railties/MIT-LICENSE
# to get tests:
# git clone http://github.com/rails/rails.git && cd rails/railties/
# git checkout v4.1.5 && tar czvf railties-4.1.5-tests.tgz test/
Source2: railties-%{version}-tests.tgz
# Default to `bundle --local` when creating a new app
# https://bugzilla.redhat.com/show_bug.cgi?id=1115079
Patch0: rubygem-railties-default-to-bundle-install-local.patch
# Let's keep Requires and BuildRequires sorted alphabeticaly
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(actionpack) = %{version}
Requires: %{?scl_prefix}rubygem(activesupport) = %{version}
Requires: %{?scl_prefix_ruby}rubygem(rake)
Requires: %{?scl_prefix_ruby}rubygem(thor) >= 0.18.1
Requires: %{?scl_prefix_ruby}rubygem(thor) < 2.0
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby(release)
%if 0%{?runtests}
BuildRequires: %{?scl_prefix}rubygem(actionpack) = %{version}
BuildRequires: %{?scl_prefix}rubygem(actionview) = %{version}
BuildRequires: %{?scl_prefix}rubygem(activerecord) = %{version}
BuildRequires: %{?scl_prefix}rubygem(activesupport) = %{version}
BuildRequires: %{?scl_prefix}rubygem(actionmailer) = %{version}
BuildRequires: %{?scl_prefix_ruby}rubygem(bundler)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix_ruby}rubygem(rake)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix_ruby}rubygem(thor) >= 0.18.1
BuildRequires: %{?scl_prefix_ruby}rubygem(thor) < 2.0
%endif
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Rails internals: application bootup, plugins, generators, and rake tasks.
Railties is responsible to glue all frameworks together. Overall, it:
* handles all the bootstrapping process for a Rails application;
* manager rails command line interface;
* provides Rails generators core;

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description doc
This package contains documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{_bindir}
%{?scl:scl enable %scl - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0 -p1
popd

# May by only for v.3.0.3-6
#  
# Some stylesheet seems to be mistakingly marked as executable in the upstream
# source
find .%{gem_instdir} -name *.css -type f -perm /a+x -exec %{__chmod} -v 644 {} \;

%build

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}
cp -a .%{_bindir}/* %{buildroot}%{_bindir}

cp %{SOURCE1} %{buildroot}%{gem_instdir}

%check
%if 0%{?runtests}
# fake RAILS_FRAMEWORK_ROOT
ln -s %{gem_dir}/gems/activesupport-%{version}/ .%{gem_dir}/gems/activesupport
ln -s %{gem_dir}/gems/actionmailer-%{version}/ .%{gem_dir}/gems/actionmailer
ln -s ${PWD}%{gem_instdir} .%{gem_dir}/gems/railties
touch .%{gem_dir}/gems/load_paths.rb
touch .%{gem_dir}/gems/Gemfile
export RUBYOPT="-I${PWD}%{gem_dir}/gems/railties:${PWD}%{gem_dir}/gems/railties/lib:${PWD}%{gem_dir}/gems/railties/test"
export PATH="${PWD}%{gem_dir}/gems/railties/bin:$PATH"

pushd .%{gem_dir}/gems/railties
# extract tests
tar xzf %{SOURCE2}

# Get rid of Bundler for now
sed -i -e "s|require 'bundler/setup' unless defined?(Bundler)||" test/isolation/abstract_unit.rb

# TODO: Test are not yet in the best state.
#       Investigate: Very unstable, more failures than in Fedora
%{?scl:scl enable %{scl} - << \EOF}
ruby -I. -e 'Dir.glob("test/**/*_test.rb").sort.each {|t| require t}' \
  | grep "101. runs, .* assertions, .* failures, 33.* errors, 0 skips"
%{?scl:EOF}
popd
%endif

%files
%{_bindir}/rails
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/RDOC_MAIN.rdoc
%doc %{gem_instdir}/README.rdoc

%changelog
* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to 4.1.5

* Wed Jul 23 2014 Josef Stribny <jstribny@redhat.com> - 4.0.2-3
- Patch: Run bundle install with --local when creating new app
  - Resolves: rhbz#1115079

* Wed Feb 05 2014 Josef Stribny <jstribny@redhat.com> - 4.0.2-2
- Fix license (SyntaxHighlighter is removed in 4.x.x)

* Wed Dec 04 2013 Josef Stribny <jstribny@redhat.com> - 4.0.2-1
- Update to Railties 4.0.2
  - Resolves: rhbz#1037985

* Thu Nov 21 2013 Josef Stribny <jstribny@redhat.com> - 4.0.1-1
- Update to Railties 4.0.1

* Wed Oct 16 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-2
- Convert to scl.

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to Railties 4.0.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Josef Stribny <jstribny@redhat.com> - 3.2.13-1
- Fix license.

* Sat Mar 09 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.12-3
- Relax RDoc dependency.

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.12-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 12 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.12-1
- Update to Railties 3.2.12.

* Wed Jan 09 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.11-1
- Update to Railties 3.2.11.

* Fri Jan 04 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.10-1
- Update to Railties 3.2.10.

* Mon Aug 13 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.8-1
- Update to Railties 3.2.8.

* Mon Jul 30 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.7-1
- Update to Railties 3.2.7.

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.6-1
- Update to Railties 3.2.6.
- Move some files into -doc subpackage.
- Remove the unneeded %%defattr.
- Introduce %%check section (not running tests yet, as they are part of dependency loop).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.15-1
- Update to Railties 3.0.15.

* Fri Jun 01 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.13-1
- Update to Railties 3.0.13.

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.0.11-1
- Rebuilt for Ruby 1.9.3.
- Update to Railties 3.0.11.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.10-1
- Update to Railties 3.0.10

* Thu Jul 21 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.9-2
- Added missing RDoc dependency.

* Thu Jul 07 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.9-1
- Update to Railties 3.0.9

* Mon Jun 27 2011  <mmorsi@redhat.com> - 3.0.5-2
- include fix for BZ #715385

* Tue Mar 29 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.5-1
- Updated to Railties 3.0.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011  <Minnikhanov@gmail.com> - 3.0.3-7
- Fix Comment 11 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=668090#c11
- Take LICENSE file from upstream.

* Mon Jan 31 2011  <Minnikhanov@gmail.com> - 3.0.3-6
- Fix Comment 9 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=668090#c9
- Temporarily test suite is blocked.

* Thu Jan 27 2011  <Minnikhanov@gmail.com> - 3.0.3-5
- Fix Comment 7 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=668090#c7 

* Tue Jan 25 2011  <Minnikhanov@gmail.com> - 3.0.3-4
- Fix Comment 5 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=668090#c5 

* Mon Jan 24 2011  <Minnikhanov@gmail.com> - 3.0.3-3
- Fix Comment 3 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=668090#c3 

* Sun Jan 23 2011  <Minnikhanov@gmail.com> - 3.0.3-2
- Fix Comment 1 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=668090#c1 

* Fri Jan 07 2011  <Minnikhanov@gmail.com> - 3.0.3-1
- Initial package
