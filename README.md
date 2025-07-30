1. Data Collection
   
11.MalwareHashesAcquisition.py : 

To extract a list of SHA-256 hashes that represent known malware samples the MalwareBazaar API. 

12.PreviouslyDownloadedIdentification.py:

To avoid redundant downloads, the system scans a designated local directory where previously acquired  samples are stored. 

13.NewHashestoDownload.py :

A set difference operation is performed between the full list of available hashes and the list of previously downloaded hashes. 

14.SampleDownloader.py:

Each unique hash is used to query the MalwareBazaar API for the corresponding  sample.

15.OrganizeHashesbyTypes.py

 All downloaded files are organized by file extension. We have used dll_files.txt in our research software.

2.  Behavioral Feature Extraction Methodology

   21.CalculateRemainingBehaviourDLL.py
   
To optimize API utilization and avoid redundant queries, a differential analysis is conducted between the list of all collected malware samples and those for which behavioral data has already been acquired. 

22. BehavioralDataRetrieval.py

An automated retrieval process is implemented to extract behavioral reports from VirusTotal. Using a pool of API keys, 

23.ExtractSandboxwiseBehavior

To facilitate structured analysis, sandbox-specific behavior entries are extracted from each JSON response and saved in directories categorized by sandbox engine.

3.DLLLabelExtraction
31.31.CalculateRemainingLabels.py
32.getDLLLabel

The Malicious DLL Label Extraction Module is designed to automate the identification and labeling of malicious Dynamic Link Libraries (DLLs) by querying the VirusTotal intelligence service 

33.ExtractLabel
This script processes malware scan results from VirusTotal, extracting detection labels from a specified set of antivirus (AV) engines (e.g., AVG, Fortinet, Ikarus, Kaspersky, Microsoft).

4.DLLFeatureExtraction

41.ReadBERTBehaviour.py

The extracted behavioral indicators—including file system activity, registry modifications, process creation, memory-resident domain artifacts, and HTTP communications—were converted into structured sequences
suitable for input into sequence-based models.

42.MergeBERTSeqLabel.py

Merge sequence with extracted malware families: Agentc, Emotet, Dridex, and Yakes,

43.dropFreqThreshold.py

drop classes with frequency less than threshold 

44.extractUnique.py

visualize the feature frequencies



DLLBERTSeqFinal.ipynb

This Colab notebook will run on google Colab

the performance of four Transformer-based models \textbf{RoBERTa}, \textbf{BERT}, \textbf{DistilBERT}, and \textbf{ALBERT} on the classification of malicious Dynamic Link Library (DLL) samples.

<img width="3546" height="1730" alt="grouped_final_metrics_barplot" src="https://github.com/user-attachments/assets/697d3ed7-f345-4e4d-973a-2689dc0c5237" />
