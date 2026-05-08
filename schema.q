/ schema.q - Defines the table structures

trade:([] time:`timespan$(); sym:`symbol$(); price:`float$(); size:`long$());
quote:([] time:`timespan$(); sym:`symbol$(); bid:`float$(); ask:`float$(); bsize:`long$(); asize:`long$());
