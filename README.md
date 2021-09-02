# InputGenerator
Generating labeling instances as a set of 2D points in a bounded plane. <br />
Each point is assigned with a label text
Format (like DIMACS FORMAT)<br />
Files are assumed to be well-formed and internally consistent: coordinates are valid (inside the plane range), points are defined uniquely (different pairs of coordinates).<br />  
## Comment line:

Comment lines give human-readable information about the file and are ignored by programs.<br /> 
Comment lines can appear at beginning in the file. <br />
Each comment line begins with a lower-case character c. <br />
c This is an example of a comment line.<br />



## Label line:

There is one label line per input file. The problem line must appear before the problem line. The label line has the following format. <br />
The lower-case character l signifies that this is the label line.  The number of the fields x.label should be consitently egal to the number of labels assigned in the Descriptor lines.<br />
l 1.label  2.label 3.label ...<br />



## Problem line:

There is one problem line per input file. The problem line must appear before any descriptor lines. The problem line has the following format. <br />
The lower-case character p signifies that this is the problem line. The FORMAT field is for specifiying different Categories, and should contain the word "UNWEIGHTED", "WEIGHTED" and so on. The field number_of_nodes should be consitently egal to the number of Descriptor lines.<br />
p FORMAT number_of_nodes plane_width plane_height<br />


## Descriptor line:

There is one descriptor line for each point element, each with the following format. Each point (x,y) of label_index appears exactly once in the input file. <br />
Each element descriptor line terminated with 0.<br /> 
x y label_index 0 <br />

