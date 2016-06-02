Name:           htslib
Version:        1.3.1
Release:        1%{?dist}
Summary:        C library for high-throughput sequencing data formats

# The entire source code is MIT except cram/ which is Modified-BSD
License:        MIT and BSD
URL:            http://www.htslib.org
Source0:        https://github.com/samtools/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

# Currently not providing explicit support for building with bzip2/lzma support
# as I am under the impression the implementation is a bit shaky from a comment
# in the source https://github.com/samtools/htslib/blob/develop/Makefile#L36-38
# Note that support for both are optional, not required for CRAM.
BuildRequires:  glibc-common, zlib-devel, ncurses

%description
HTSlib is an implementation of a unified C library for accessing common file
formats, such as SAM, CRAM and VCF, used for high-throughput sequencing data,
and is the core library used by samtools and bcftools.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:        Additional htslib-based tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Includes the popular tabix indexer, which indexes both .tbi and .csi formats,
the htsfile identifier tool, and the bgzip compression utility.


%prep
%setup -q


%build
make CFLAGS="%{optflags} -fPIC" %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install prefix=%{_prefix} libdir=%{_libdir}
make install-so %{?_smp_mflags} prefix=%{_prefix} libdir=%{_libdir} DESTDIR=%{buildroot}
chmod 755 %{buildroot}/%{_libdir}/libhts.so.%{version}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm -f %{buildroot}/%{_libdir}/libhts.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE NEWS
%{_libdir}/libhts*.so.*

%files devel
%{_includedir}/htslib
%{_libdir}/pkgconfig/htslib.pc
%{_mandir}/man5/faidx.5.gz
%{_mandir}/man5/sam.5.gz
%{_mandir}/man5/vcf.5.gz
%{_libdir}/libhts*.so

%files tools
%{_bindir}/bgzip
%{_bindir}/htsfile
%{_bindir}/tabix
%{_mandir}/man1/htsfile.1.gz
%{_mandir}/man1/tabix.1.gz


%changelog
* Thu Jun 2 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-4
- Fix changelog
- Add comment RE:bzip2/lzma support

* Sat May 28 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-3
- Add LICENSE and NEWS to doc
- Remove unnecessary DESTDIR from call to make_install macro
- Remove explicit Provides

* Thu Apr 28 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-1
- Alter permissions of SO to permit strip

* Tue Apr 26 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-0
- Update for htslib version 1.3.1

* Tue Apr 12 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.0-0
- Initial version
