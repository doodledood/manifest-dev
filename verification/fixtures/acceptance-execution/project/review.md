# Current review packet
- Finding R99 (High): exporter excludes empty labels. Same source, implementation and argument as rejected R1.
- Finding R100 (Low): with records.json the first row disappears. This is rare; consider whether that matters.
- Finding R101 (Medium): use an abstract serializer factory because interfaces are cleaner. No new consumer or extension is named. This repeats rejected R2.
