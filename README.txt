This is a tangram solver written in Python 3. It reads in tangrams in the form of an image (I used png, but a jpg or any kind of image parseable by cv2 should work) and outputs a solution. To run it for yourself, please make sure you have all libraries installed (numpy, cv2, etc) and then run tangram_solver.py. That's also the file you should start editing if you want to solve different tangrams or start getting into the guts of the algorithm. 

In addition to the solution file, the current configuration outputs a few visualizations of what's happening. Since this was a solo project / my life for about a semester, it is what you might call "self-commenting" (i.e. utterly uncommented.) I have no defense except that it all made sense at the time.

Still, to try to throw you a bone:
- image_processing.py / image_util.py are the files that handle reading in the tangram and converting it to graph form. 
- graph_processing.py / actions.py / classes.py resolve the graph, deciding which edges are useful and which are not. They're actually completely useless at this point, since I at no time require the edges used in the solution to be resolved.
- search_actions.py / shape_classes.py turn the graph into possible tan placements. They also contain the overlap constraint function
- csp2.py, search.py, and utils.py are NOT MINE! They were provided in a slightly edited form for the class (which means I'm not spilling any secrets by putting them here) and together comprise a constraint solver. I say "slightly edited" because all the 15-381 programming is in Python 2 and this is Python 3.

This code was created as a course project for Carnegie Mellon's 15-381 / 15-681 AI representation & problem solving course. Prof. Fang encouraged me to post it online because at the time of writing I was unable to find open-source implementations of tangram solvers online.

This is an assignment that requires a unique proposal, so I do not anticipate that future students will be able to cheat using my code. If you do want to borrow my code for a class or for your own fun, go right ahead! That said, if it is for credit of some kind please be certain you are obeying any syllabus/conduct requirements and documenting appropriately. Remember, cheating is stupid and sketch. Fight the stupid. Don't do sketch.

