#!/usr/bin/perl 
# 
# 
# 
# 
# Kim Brugger (27 Apr 2015), contact: kbr@brugger.dk

use strict;
use warnings;
use Data::Dumper;


my $pre_end = 0;

while(<>) {
  next if (/#/);
  
  my @F= split("\t");

  my $dist = $F[1] - $pre_end + 1;
  print  $dist ."\n" if ( $dist >= 1 && $dist < 4000 );
  $pre_end = $F[2];
}
