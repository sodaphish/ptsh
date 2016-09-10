use fw;
delete from dddates;
insert into dddates ( date ) select distinct date from blocked;
