F03-2 good well, seems like full data
722,848


F03-4 good well, seems like full data
442, 1007

1. Create attribute set of open myext
	add wmgym external attribute by using
	compiler: C:\Users\Polash-Dell\.conda\envs\tf_gpu\python.exe
	code: C:\Users\Polash-Dell\coder_guy\PycharmProjects\snippets\ext_attrib_?.py

	Attrib must be saved in attrib set myext
	The program runs and saves as a attrib there when we add as new or close

2. ext_attrib_5.py grabs csv for poro and 1_original_seismic

3. aws_sagemaker_tensorflow_train2.py uses aws_entry_seis_poro_tf2.py to build model from data in S3


4. create and launch endpoint. see aws_sagemaker_tensorflow1.py.


Now
5. aws_sagemaker_tensorflow_test3. see what the fuckis wrong.
6. create full poro vol from endpoint using 1_original_seismic as input
7. Combile to full code from broiler plate.

