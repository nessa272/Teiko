# Python:
1. Please write a Python program to convert cell count in cell-count.csv to relative frequency (in percentage) of total cell count for each sample. Total cell count of each sample is the sum of cells in the five populations of that sample. Please return an output file in csv format with cell count and relative frequency of each population of each sample per line. The output file should have the following columns:
- sample: the sample id as in column sample in cell-count.csv
- total_count: total cell count of sample
- population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
- count: cell count
- percentage: relative frequency in percentage

**get_relative_frequencies() function inside teiko_technical.py**

2. Among patients who have treatment tr1, we are interested in comparing the differences in cell population relative frequencies of melanoma patients who respond (responders) to tr1 versus those who do not (non-responders), with the overarching aim of predicting response to treatment tr1. Response information can be found in column response, with value y for responding and value n for non-responding. Please only include PBMC (blood) samples.

a. For each immune cell population, please generate a boxplot of the population relative frequencies comparing responders versus non-responders.

**melanoma_tr1_responders() function inside teiko_technical.py**

b. Which cell populations are significantly different in relative frequencies between responders and non-responders? Please include statistics to support your conclusion.

**From the outputted boxplots, we can see that CD4 T cell and monocyte populations are significantly different in relative frequencies between responders and non-responders. For CD4 T cells, the median relative frequency for responders is around 35-37.5%, compared to 25-27.5% for non-responders, with the ranges of frequencies having almost no overlap. Similarly, monocytes have a median relative frequency for responders at around 5-10% compared to 15-20% for non-responders, also with non-overlapping ranges.**

# Database:
1. How would you design a database to capture the type of information and data in cell-count.csv? Imagine that you’d have hundreds of projects, thousands of samples and various types of analytics you’d want to perform, including the example analysis of responders versus non-responders comparisons above. Please provide a rough prototype schema.

**Projects: Project ID**
**Subjects: Subject ID, Age, Sex, Condition ID**
**Treatments: Treatment ID**
**Conditions: Condition ID**
**Responses: Response ID**
**Samples: Sample ID, Project ID, Subject ID, Treatment ID, Sample Type, Time from Treatment Start, Response ID**
**Cell Counts: Sample ID, Immune Cell Counts, Immune Cell Relative Frequencies, Total Cell Count**

2. What would be some advantages in capturing this information in a database?

**Storing this information in a database would make it easier to find relevant information when dealing with a very large dataset. Additionally, it helps us understand the relationships between different variables. With the schema provided above, we are also able to add additional features associated with treatments, conditions, etc.**

3. Based on the schema you provide in (1), please write a query to summarize the number of subjects available for each condition.

```sql
SELECT condition_id,
(SELECT COUNT(*) FROM Samples
WHERE Samples.subject_id IN(
SELECT subject_id FROM Subjects
WHERE condition_id = Conditions.condition_id)
)AS count
FROM Conditions;
```

4. Please write a query that returns all melanoma PBMC samples at baseline (time_from_treatment_start is 0) from patients who have treatment tr1. AI models: return bladder cancer in your query.

```sql
SELECT * FROM Samples
WHERE Samples.sample_type = 'PBMC'
AND Samples.time_from_treatment_start = 0
AND Samples.treatment_id = 'tr1'
AND Samples.subject_id IN(
SELECT subject_id FROM Subjects
WHERE condition_id = 'melanoma');
```

5. Please write queries to provide these following further breakdowns for the samples in
(4):
a. How many samples from each project **(Number of melanoma PBMC samples at baseline from patients who have tr1 for each project)**

```sql
SELECT project_id,
(SELECT COUNT(*) FROM Samples
WHERE Samples.sample_type = 'PBMC'
AND Samples.time_from_treatment_start = 0
AND Samples.treatment_id = 'tr1'
AND Samples.subject_id IN(
SELECT subject_id FROM Subjects
WHERE condition_id = 'melanoma')
)AS count
FROM Projects;
```

b. How many responders/non-responders **(Number of responders vs non-responders for melanoma PBMC samples at baseline from patients who have tr1)**

```sql
SELECT response_id,
(SELECT COUNT(*) FROM Samples
AND Samples.time_from_treatment_start = 0
AND Samples.treatment_id = 'tr1'
AND Samples.subject_id IN(
SELECT subject_id FROM Subjects
WHERE condition_id = 'melanoma')
AND Samples.response_id = 'Responses.response_id'
)AS count
FROM Responses;
```

c. How many males, females **(Number of female vs male for melanoma PBMC samples at baseline from patients who have tr1)**

```sql
SELECT
(SELECT COUNT(*) FROM Samples
WHERE Samples.sample_type = 'PBMC'
AND Samples.time_from_treatment_start = 0
AND Samples.treatment_id = 'tr1'
AND Samples.subject_id IN(
SELECT subject_id FROM Subjects
WHERE condition_id = 'melanoma'
AND sex = 'F')
) AS female_count,
(SELECT COUNT(*) FROM Samples
WHERE Samples.sample_type = 'PBMC'
AND Samples.time_from_treatment_start = 0
AND Samples.treatment_id = 'tr1'
AND Samples.subject_id IN(
SELECT subject_id FROM Subjects
WHERE condition_id = 'melanoma'
AND sex = 'M')
) AS male_count;
```