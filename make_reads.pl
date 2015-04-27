#!/usr/bin/perl 
# 
# 
# 
# 
# Kim Brugger (11 Mar 2015), contact: kbr@brugger.dk

use strict;
use warnings;
use Data::Dumper;

my $INSERT_SIZE = 300;
my $FRAG_SIZE   = 150;

my $infile = shift;
my $fh = open_file( $infile );

open (my $fh1, " | gzip > gene_regions.1.fq.gz");
open (my $fh2, " | gzip > gene_regions.2.fq.gz");

my ( $name, $seq );

while (<$fh>) { 
  chomp;


  if ( /\>/ ) {
    if ( $name ) {
      print "$name \n";
      print_reads( $name, $seq );
    }

    $name = $_;
    $seq = "";
  }
  else {
    $seq .= $_
  }
}

if ( $name ) {
  print_reads( $name,  $seq );
}


      close( $fh1 );
      close( $fh2 );


# 
# 
# 
# Kim Brugger (11 Mar 2015)
sub print_reads {
  my ($name, $seq ) = @_;
  
  for (my $i = 0; $i < length( $seq ) - $INSERT_SIZE  - $FRAG_SIZE - 1; $i++) {

    my ( $r1_start, $r1_end ) = ($i, $FRAG_SIZE );

    my $region1 = substr( $seq, $r1_start, $r1_end );
    print $fh1 ">$name-$i\n$region1\n";

    my ( $r2_start, $r2_end ) = ($i+ $INSERT_SIZE, $FRAG_SIZE);
    my $region2 = substr( $seq, $r2_start, $r2_end );
    print $fh2 ">$name-$i\n$region2\n";
  }
    
  
}


# 
# 
# Kim Brugger (03 Aug 2011)
sub open_file {
  my ($filename) = @_;

  my $fh;

  if ( $filename =~ /gz/) {
    CORE::open ( $fh, "gunzip -c $filename | ") || die "Could not open '$filename': $!\n";
  }
  else {
    CORE::open ( $fh, "$filename") || die "Could not open '$filename': $!\n";
  }

  return $fh;
  
}


