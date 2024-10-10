# Repositories

[**COSC425-DATA**](https://github.com/SpencerPresley/COSC425-DATA)
- This repository contains the code used to extract and analyze various statistics from exported Web of Science records. It also contains the prototype AI system.

[**COSC425-FRONT**](https://github.com/SpencerPresley/COSC425-FRONT)
- This repository contains the code for the front-end of the COSC425 project. The front-end is build using Next.js App directory with Typescript. It pulls the data from a JSON file stored in a AWS S3 bucket. The JSON file is the resulting output from the COSC425-DATA repository.

[**426-Taxonomy-Generator**](https://github.com/SpencerPresley/426-Taxonomy-Generator)
- This repository contains the code for parsing through an excel file and formatting it into a JSON file. The excel file is from NCSES and contains data on PhD fields of study, ranking them into a hierarchy from most broad to most specific. The JSON file is the hierarchy with the field names as keys and the parent field names as values.

[**426-AI**](https://github.com/SpencerPresley/426-AI)
- This repository contains the code for the AI system used to analyze the abstracts. It consists of several chains that work together to analyze and classify the abstracts into the aformentioned taxonomy. 
