Name:           htslib
Version:        1.3.1
Release:        1%{?dist}
Summary:        C library for high-throughput sequencing data formats

# The entire source code is MIT except cram/ which is Modified-BSD
License:        MIT and BSD
URL:            http://www.htslib.org
Source0:        https://github.com/samtools/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  glibc-common, zlib-devel, ncurses
Provides:	libhts.so.1()(64bit)

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
%make_install prefix=%{_prefix} libdir=%{_libdir} DESTDIR=%{buildroot}
make install-so %{?_smp_mflags} prefix=%{_prefix} libdir=%{_libdir} DESTDIR=%{buildroot}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm -f %{buildroot}/%{_libdir}/libhts.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc
%{_libdir}/libhts*.so.*

%files devel
%doc
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
* Tue Apr 26 2016 Sam Nicholls <sam.n@studio8media.co.uk> - 1.3.1-1
- Initial version
- 
