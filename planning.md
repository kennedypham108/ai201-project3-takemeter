# Project 3 Planning Document

## Community

I chose the r/nba subreddit, focusing specifically on posts and comments about LeBron James. This community is a good fit for a classification task because discussions about LeBron vary widely in quality and style. Some users provide statistics, game evidence, salary-cap information, or historical comparisons, while others give reasoned opinions or post emotional reactions and exaggerated hot takes. These distinctions matter in r/nba because users regularly debate whether a basketball claim is supported, thoughtful, or mostly based on emotion.

## Label Taxonomy

I will use three mutually exclusive labels: **Evidence-Based Analysis**, **Reasoned Opinion**, and **Hot Take or Reaction**.

### 1. Evidence-Based Analysis

A post or comment belongs to this label when it supports its main claim with specific evidence, such as statistics, game performance, salary information, roster construction, historical comparison, or another concrete and checkable detail.

**Example 1:**
“LeBron is still valuable because he averaged over 20 points per game while maintaining efficient shooting.”

**Example 2:**
“The Lakers should be careful about giving LeBron another maximum contract because it would reduce their salary-cap flexibility around Luka.”

### 2. Reasoned Opinion

A post or comment belongs to this label when it gives a clear position and an understandable explanation but does not rely heavily on statistics or specific evidence.

**Example 1:**
“LeBron should retire as a Laker because that is where he spent the final major chapter of his career.”

**Example 2:**
“A return to Cleveland for one final season would be the best ending because it would bring his career full circle.”

### 3. Hot Take or Reaction

A post or comment belongs to this label when it is mainly emotional, exaggerated, insulting, celebratory, sarcastic, or unsupported by meaningful reasoning.

**Example 1:**
“LeBron is completely washed and any team paying him is finished.”

**Example 2:**
“He is over 40 and still owns the entire league. He is not human.”

## Hard Edge Cases

The hardest edge cases will occur between **Evidence-Based Analysis** and **Reasoned Opinion**. Some comments may include basketball reasoning but no statistics or concrete examples. For example, “LeBron is still a top player because he controls the offense” gives a reason, but it does not provide specific evidence. I will label this as **Reasoned Opinion** unless the comment includes at least one concrete, checkable detail.

Another difficult boundary will occur between **Reasoned Opinion** and **Hot Take or Reaction**. A short comment such as “LeBron is still better than almost everyone” may sound like an opinion, but without explanation it is mostly unsupported. I will label a post as **Reasoned Opinion** only if it gives a clear reason. If it gives only a claim, insult, joke, emotional reaction, or exaggeration, I will label it **Hot Take or Reaction**.

When a post includes both opinion and evidence, I will use the strongest qualifying label. If a post contains concrete evidence that directly supports the claim, it will be labeled **Evidence-Based Analysis**. If it contains reasoning but no concrete evidence, it will be labeled **Reasoned Opinion**. If it contains neither meaningful evidence nor explanation, it will be labeled **Hot Take or Reaction**.

## Data Collection Plan

I will collect at least 200 public posts or comments from r/nba threads about LeBron James. I will search for discussions involving LeBron’s retirement, Lakers contract, possible trades, Luka Doncic, Cleveland, Golden State, age, longevity, salary, defense, playoff performance, legacy, the GOAT debate, and Bronny James.

I will treat each individual post or comment as one example. I will not label an entire Reddit thread as a single example. I will store the data in a CSV file with columns such as:

- `text`
- `label`
- `source_url`
- `notes`

My target distribution is:

- 70 Evidence-Based Analysis examples
- 65 Reasoned Opinion examples
- 65 Hot Take or Reaction examples

This gives me 200 total examples while keeping every label above 20% of the dataset. If one label is underrepresented after the first 200 examples, I will collect additional examples from threads that are more likely to contain that label. For example, I will use game-analysis and salary-cap threads to find more Evidence-Based Analysis, legacy and retirement threads to find more Reasoned Opinion, and game-reaction or controversial debate threads to find more Hot Take or Reaction examples.

After collection, I will split the dataset into training, validation, and test sets. I plan to use approximately 70% for training, 15% for validation, and 15% for testing. I will use a stratified split so that all three labels appear in similar proportions in each set.

## Evaluation Metrics

I will evaluate both the fine-tuned DistilBERT model and the zero-shot Groq baseline on the same test set.

I will report:

- Overall accuracy
- Precision for each label
- Recall for each label
- F1 score for each label
- Macro-averaged F1 score
- Confusion matrix

Accuracy is useful because it shows the percentage of total predictions that are correct, but accuracy alone is not enough. A model could achieve a high accuracy by predicting the most common label too often. Per-class precision, recall, and F1 will show whether the model performs well on each label instead of only the largest category.

Macro F1 is especially important because it gives each label equal weight. This will help show whether the model can distinguish analysis, opinion, and hot takes fairly. The confusion matrix will show which labels are most often confused, especially whether the model struggles between Evidence-Based Analysis and Reasoned Opinion or between Reasoned Opinion and Hot Take or Reaction.

## Definition of Success

I will consider the fine-tuned classifier successful if it reaches at least:

- 75% overall test accuracy
- 0.70 macro F1
- At least 0.65 F1 for every individual label
- Better overall accuracy or macro F1 than the zero-shot Groq baseline

For a real community tool, I would consider the classifier good enough for deployment if it reaches at least 80% accuracy, at least 0.75 macro F1, and no individual label has an F1 score below 0.70. I would also want the confusion matrix to show that errors are not concentrated heavily in one category.

The classifier would be useful as a discussion-analysis tool, not as an automatic moderation system. Its purpose would be to help summarize the types of LeBron discussion in r/nba, not to remove posts or punish users.

## AI Tool Plan

### Label Stress-Testing

Before labeling all 200 examples, I will give an AI tool my three label definitions and ask it to generate 5–10 difficult examples that sit near the boundary between two labels. I will focus especially on the boundary between Evidence-Based Analysis and Reasoned Opinion, and the boundary between Reasoned Opinion and Hot Take or Reaction.

I will try to classify each generated example using my written rules. If several examples cannot be labeled consistently, I will revise the definitions before continuing with annotation. I will document any changes I make to the taxonomy.

### Annotation Assistance

I may use an LLM to suggest preliminary labels for a small batch of examples, but I will manually review every label before including it in the final dataset. The AI suggestion will not be treated as the final answer.

If I use AI pre-labeling, I will add a column such as `ai_suggested_label` or `prelabeled_by_ai` to track which examples received AI assistance. I will disclose this process in the README and AI usage section. The final `label` column will always represent my reviewed decision.

### Failure Analysis

After evaluating the models, I will provide the list of incorrect predictions to an AI tool and ask it to identify possible error patterns. I will look for patterns such as:

- Short posts being mislabeled as Hot Take or Reaction
- Statistics being detected even when they do not support the main claim
- Sarcastic comments being mistaken for literal opinions
- Reasoned Opinion being confused with Evidence-Based Analysis
- Strong emotional language causing otherwise analytical posts to be mislabeled

I will not automatically accept the AI’s conclusions. I will manually inspect the examples connected to each suggested pattern and only report patterns that are supported by multiple real errors.

## Stretch Features

I am not planning to begin any stretch features until the required project is complete. If I decide to add inter-annotator reliability, confidence calibration, error pattern analysis, or a deployed interface, I will update this planning document before starting that feature.
