#Q22

##Study the depth of a binary search tree under various operations and proportions of operations and insertion models such as random. We have seen that the height of a binary search tree depends also on the nature and sequence of operations performed. Study interesting sequences of operations and see how the height varies. Back up with experimental observations.

`
-------------------------------------------------------------------------------------------------------------------------------------


List of Files ::

1. main.cpp -- this contains code for comparing all the BST with other versions of BST like AVL, Splay and RB. Here we compare the 				   time taken to Initialize (Build) the tree, Time taken for each to get the height of the tree, Time taken to search 				   for all the elements given in a Random Fashion. 
			   -- Note -- No deletion operation perfromed, only Insertion and search are performed!		

2. main_delete.cpp -- this contains code for comparing all the BST with other versions of BST like AVL, Splay and RB. Here we 							  compare the time taken to Initialize (Build) the tree and Delete the nodes in different pattens. The patterns 					  include first insert some nodes then delete half of them, or, simlarly one more was to insert some nodes 							  delete all, insert again and so on... These kind of different patterns was considered for testing.
`

Now, the main part of the project goes into Generating Patterns , we have discussed that part in a very detailed manner in our report.

Now, We have generated a total of 9 different patterns to test our programs. You can see them in Test_Patterns directory.

They are labelled in an intuative format for better understannding.

Generating Patterns python scrip is attached in Generating_Patterns folder in .ipynb

`


For testing, The " tree.h " file contains all the function and list of parameters they need, so for testing one needs to just call them, rest is abstract. 

For testing purpose the above inputs --- 
	 
	 For -- (main.cpp)  -- Insert and Search

	 $ g++ -o main main.cpp

	 $ ./main < Test_Parrerns/Decreasing/decreasing.txt

Similarly all the .txt files for insertion has the same name as the folder name....

 
	 For -- (main_delete.cpp)  -- Insert and Search

	 $ g++ -o main_delete main.cpp

	 $ ./main_delete < Test_Parrerns/Decreasing/decreasing-delete-random.txt


Similarly, for delete patterns all the files have a prefix of -- 

   -delete-inc-dec.txt       -- Delete in incresing_decreasing patterns

   -delete-increasing.txt    -- Delete in increasing pattern (sorted order)

   -delete-random.txt        -- Delete elements in Random pattern

   -delete-decreasing.txt    -- Delete elements in decreasing pattern

We have tested pattens to be deleted in 4 ways as mentioned order..

`

