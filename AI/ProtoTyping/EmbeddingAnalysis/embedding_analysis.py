from numpy import dot
from numpy.linalg import norm
from dotenv import load_dotenv
import os
from itertools import combinations
from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import (
    load_evaluator,
    EmbeddingDistance,
    EmbeddingDistanceEvalChain,
)
from tabulate import tabulate  # For table formatting
import matplotlib.pyplot as plt
import numpy as np

# Load environment variables
load_dotenv()


class EmbeddingAnalysis:
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-large",
        file_name: str = "similarity_results.txt",
        plt_prefix="analysis_",
        save_dir: str = "Plots/Analysis_1",
    ):
        print("Initializing EmbeddingAnalysis...")
        self.file_name = file_name
        self.plt_prefix = plt_prefix
        self.save_dir = save_dir
        self.api_key = api_key
        self.model = model
        self.openai_embeddings = OpenAIEmbeddings(
            openai_api_key=self.api_key, model=self.model
        )
        self.embeddings = {}
        self.similarity_results = {}

        # Evaluators
        print("Loading evaluators...")
        self.cosine_similarity_evaluator = EmbeddingDistanceEvalChain(
            distance_metric=EmbeddingDistance.COSINE, embeddings=self.openai_embeddings
        )

        self.euclidean_distance_evaluator = EmbeddingDistanceEvalChain(
            distance_metric=EmbeddingDistance.EUCLIDEAN,
            embeddings=self.openai_embeddings,
        )

        self.manhattan_distance_evaluator = EmbeddingDistanceEvalChain(
            distance_metric=EmbeddingDistance.MANHATTAN,
            embeddings=self.openai_embeddings,
        )

        self.chebyshev_distance_evaluator = EmbeddingDistanceEvalChain(
            distance_metric=EmbeddingDistance.CHEBYSHEV,
            embeddings=self.openai_embeddings,
        )

        self.hamming_distance_evaluator = EmbeddingDistanceEvalChain(
            distance_metric=EmbeddingDistance.HAMMING, embeddings=self.openai_embeddings
        )
        print("Evaluators loaded.")

    def _run_evaluator(self, evaluator, prediction, reference):
        """Run a specific evaluator on two strings."""
        # print(f"Running evaluator: {evaluator}")

        # If prediction or reference is a list, concatenate the items into a single string
        if isinstance(prediction, list):
            prediction = " ".join(prediction)
        if isinstance(reference, list):
            reference = " ".join(reference)

        # print(f"Prediction: {prediction[:50]}... (truncated)")
        # print(f"Reference: {reference[:50]}... (truncated)")

        try:
            # Pass the concatenated strings to the evaluator
            result = evaluator.evaluate_strings(
                prediction=prediction, reference=reference
            )
            # print(f"Evaluator result: {result}")
            return result
        except Exception as e:
            print(f"Error running evaluator: {e}")
            raise

    def embed_strings(self, **strings):
        """Store the raw strings for evaluation, ensuring all inputs are lists."""
        print("Storing strings...")
        for key, text in strings.items():
            if isinstance(text, list):
                # Store the list as is
                print(f"Storing list for key: {key}")
                self.embeddings[key] = text
            else:
                # If it's a single string, wrap it in a list
                print(f"Storing string for key: {key}")
                self.embeddings[key] = [text]
        print("Strings stored.")
        self._calculate_all_similarities()

    def _calculate_all_similarities(self):
        """Calculate similarity for all combinations of embeddings using all evaluators."""
        print("Calculating similarities...")

        # Define weights for cosine similarity and distance metrics
        cosine_weight = 0.5
        distance_weight = 0.5

        # Loop over all combinations of embeddings
        for (key1, emb1_list), (key2, emb2_list) in combinations(
            self.embeddings.items(), 2
        ):
            print(
                f"Comparing {key1} and {key2}"
            )  # Debugging: Print each comparison being generated

            similarities = []
            for emb1 in emb1_list:
                for emb2 in emb2_list:
                    print(
                        f"Running evaluators for list items: {emb1[:5]}... and {emb2[:5]}..."
                    )  # Debugging

                    # Calculate multiple metrics
                    cosine_result = self._run_evaluator(
                        self.cosine_similarity_evaluator, emb1, emb2
                    )
                    euclidean_result = self._run_evaluator(
                        self.euclidean_distance_evaluator, emb1, emb2
                    )
                    manhattan_result = self._run_evaluator(
                        self.manhattan_distance_evaluator, emb1, emb2
                    )
                    chebyshev_result = self._run_evaluator(
                        self.chebyshev_distance_evaluator, emb1, emb2
                    )
                    hamming_result = self._run_evaluator(
                        self.hamming_distance_evaluator, emb1, emb2
                    )

                    # Normalize distance metrics (optional, depending on your scale)
                    normalized_euclidean = (
                        1 / (1 + euclidean_result["score"])
                        if euclidean_result and "score" in euclidean_result
                        else None
                    )

                    # Combine cosine similarity and distance metrics using weights
                    combined_score = None
                    if cosine_result and "score" in cosine_result:
                        combined_score = (cosine_weight * cosine_result["score"]) + (
                            distance_weight * normalized_euclidean
                            if normalized_euclidean is not None
                            else 0
                        )

                    # Calculate percentage drop between cosine similarity and combined score
                    percentage_drop = None
                    if cosine_result and combined_score is not None:
                        percentage_drop = (
                            (cosine_result["score"] - combined_score)
                            / cosine_result["score"]
                        ) * 100

                    # Store the pair of items and their similarity scores
                    similarities.append(
                        {
                            "item1": emb1,
                            "item2": emb2,
                            "cosine": (
                                cosine_result["score"]
                                if cosine_result and "score" in cosine_result
                                else None
                            ),
                            "euclidean": (
                                euclidean_result["score"]
                                if euclidean_result and "score" in euclidean_result
                                else None
                            ),
                            "manhattan": (
                                manhattan_result["score"]
                                if manhattan_result and "score" in manhattan_result
                                else None
                            ),
                            "chebyshev": (
                                chebyshev_result["score"]
                                if chebyshev_result and "score" in chebyshev_result
                                else None
                            ),
                            "hamming": (
                                hamming_result["score"]
                                if hamming_result and "score" in hamming_result
                                else None
                            ),
                            "combined_score": combined_score,
                            "percentage_drop": percentage_drop,  # Add the percentage drop to the results
                        }
                    )

            # Store the similarities with item pairs
            self.similarity_results[f"{key1}-{key2}"] = {
                "individual_similarities": similarities
            }

        print("Similarity calculations complete.")

    def available_comparisons(self):
        """Return a list of available embedding comparisons."""
        return list(self.similarity_results.keys())

    def print_comparison(self, comparison_key: str = None):
        """Print the similarity for a specific comparison or all comparisons in a table format."""
        if comparison_key:
            comparisons = [comparison_key]
        else:
            comparisons = self.similarity_results.keys()

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        first_iteration = True

        for comparison_key in comparisons:
            if comparison_key in self.similarity_results:
                results = self.similarity_results[comparison_key]

                if "individual_similarities" in results:
                    table = []
                    table_data = []
                    headers = [
                        "String 1",
                        "String 2",
                        "Cosine",
                        "Euclidean",
                        "Manhattan",
                        "Chebyshev",
                        "Hamming",
                        "Combined",
                        "Percentage Drop",
                    ]

                    for similarity in results["individual_similarities"]:
                        item1 = similarity["item1"]
                        item2 = similarity["item2"]
                        cosine = similarity["cosine"]
                        euclidean = similarity["euclidean"]
                        manhattan = similarity["manhattan"]
                        chebyshev = similarity["chebyshev"]
                        hamming = similarity["hamming"]
                        combined_score = similarity["combined_score"]
                        percentage_drop = similarity["percentage_drop"]

                        table.append(
                            [
                                item1[:50] + "...",
                                item2[:50] + "...",
                                f"{cosine:.2f}%" if cosine is not None else "N/A",
                                f"{euclidean:.2f}" if euclidean is not None else "N/A",
                                f"{manhattan:.2f}" if manhattan is not None else "N/A",
                                f"{chebyshev:.2f}" if chebyshev is not None else "N/A",
                                f"{hamming:.2f}" if hamming is not None else "N/A",
                                (
                                    f"{combined_score:.2f}%"
                                    if combined_score is not None
                                    else "N/A"
                                ),
                                (
                                    f"{percentage_drop:.2f}%"
                                    if percentage_drop is not None
                                    else "N/A"
                                ),  # Add percentage drop to the table
                            ]
                        )

                        table_data.append(
                            [
                                f"{cosine:.2f}%" if cosine is not None else "N/A",
                                f"{euclidean:.2f}" if euclidean is not None else "N/A",
                                f"{manhattan:.2f}" if manhattan is not None else "N/A",
                                f"{chebyshev:.2f}" if chebyshev is not None else "N/A",
                                f"{hamming:.2f}" if hamming is not None else "N/A",
                                (
                                    f"{combined_score:.2f}%"
                                    if combined_score is not None
                                    else "N/A"
                                ),
                                (
                                    f"{percentage_drop:.2f}%"
                                    if percentage_drop is not None
                                    else "N/A"
                                ),  #
                            ]
                        )

                    mode = "w" if first_iteration else "a"
                    first_iteration = False

                    # Convert table to numpy array
                    np_table = np.array(table_data)

                    # Create a figure and axis
                    fig, ax = plt.subplots(
                        figsize=(12, len(table) * 0.5 + 1)
                    )  # Adjust height based on number of rows
                    ax.axis("tight")
                    ax.axis("off")

                    # Add the title (String 1 and String 2) above the table
                    fig.text(
                        0.5,
                        0.85,
                        f"String 1: {item1[:50]}...",
                        ha="center",
                        fontsize=12,
                        weight="bold",
                    )
                    fig.text(
                        0.5,
                        0.75,
                        f"String 2: {item2[:50]}...",
                        ha="center",
                        fontsize=12,
                        weight="bold",
                    )

                    table_plt = ax.table(
                        cellText=np_table,
                        colLabels=headers[2:],
                        cellLoc="center",
                        loc="center",
                    )

                    # Adjust table properties
                    table_plt.auto_set_font_size(False)
                    table_plt.set_fontsize(10)
                    table_plt.scale(1.2, 1.2)  # Scale table for better readability

                    # Save the figure as an image
                    image_file_name = f"{self.save_dir}/{self.plt_prefix}{comparison_key}_{item1[:10]}_{item2[:10]}.png"
                    plt.savefig(image_file_name, bbox_inches="tight")
                    plt.close(fig)  # Close the figure to free memory

                    print(f"Table saved as image: {image_file_name}")

                    print(f"Numpy table image saved as {image_file_name}")

                    with open(self.file_name, mode) as file:
                        file.write(f"Comparison: {comparison_key.upper()}\n")
                        file.write(
                            tabulate(
                                table,
                                headers=[
                                    "String 1",
                                    "String 2",
                                    "Cosine",
                                    "Euclidean",
                                    "Manhattan",
                                    "Chebyshev",
                                    "Hamming",
                                    "Combined",
                                    "Percentage Drop",
                                ],
                                tablefmt="grid",
                            )
                        )
                        file.write("\n\n\n")
                        print(f"Table written to file: {self.file_name}")

                    # Print the table with the new column
                    print(f"Comparison: {comparison_key}")
                    print(
                        tabulate(
                            table,
                            headers=[
                                "String 1",
                                "String 2",
                                "Cosine",
                                "Euclidean",
                                "Manhattan",
                                "Chebyshev",
                                "Hamming",
                                "Combined",
                                "Percentage Drop",
                            ],
                            tablefmt="grid",
                        )
                    )

    def __str__(self):
        """Return a string representation of all embeddings and their similarities."""
        result = "Embeddings:\n"
        for key, embedding in self.embeddings.items():
            if isinstance(embedding, list):
                result += f"{key}: {len(embedding)} items embedded\n"
            else:
                result += f"{key}: {embedding[:5]}... (truncated)\n"  # Truncate for readability
        result += "\nSimilarities:\n"
        for comparison in self.similarity_results.keys():
            result += f"{comparison}\n"
        return result


if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the EmbeddingAnalysis object
    analysis = EmbeddingAnalysis(
        api_key=openai_api_key,
        file_name="accurate_similarity_results.txt",
        plt_prefix="analysis_1_",
        save_dir="Plots/Analysis_1",
    )

    # Store multiple strings and lists
    analysis.embed_strings(
        top_categories=["Social and Information Sciences", "Business and Management"],
        mid_categories=[
            "Organizational Behavior",
            "Human Resource Management",
            "Workplace Psychology",
            "Leadership and Management",
            "Performance Management and Appraisal",
            "Human Resource Development",
            "Organizational Behavior and Development",
            "Organizational Theory",
        ],
        # low_categories=[
        #     "Employee Engagement",
        #     "Organizational Commitment",
        #     "Career Development",
        #     "Performance Evaluation",
        # ],
        themes=[
            "Employee Engagement",
            "Organizational Commitment",
            "Career Development",
            "Performance Evaluation",
        ],
        wos_categories=[
            "Psychology, Applied: Applied psychology is the use of psychological methods and findings of scientific psychology to solve practical problems of human and animal behavior and experience. Some of the areas of applied psychology include clinical psychology, counseling psychology, industrial and organizational psychology, forensic psychology, and sports psychology."
        ],
        title=[
            "Managers' Assessments of Employees' Organizational Career Growth Opportunities: The Role of Extra-Role Performance, Work Engagement, and Perceived Organizational Commitment"
        ],
        abstract=[
            "This study examined the role of perceived organizational commitment on managers' assessments of employees' career growth opportunities. Based on a paired sample of 161 legal secretaries and their managers, results indicated that managers used the attitudes and behaviors displayed by employees (strong extra-role performance and enhanced work engagement) as cues from which to base their perceptions of employees' affective commitment to the organization. In turn, employees perceived as highly committed to the organization experienced enhanced content and structural career growth opportunities. Moreover, the relation between managers' perceptions of employees' organizational commitment and content career growth opportunities was stronger for employees perceived as also highly committed to their careers than for employees perceived as less committed to their careers."
        ],
    )

    # Print all strings and similarities
    print(analysis)

    # List available comparisons
    print("\nAvailable Comparisons:")
    print(analysis.available_comparisons())

    # Print a specific comparison
    # analysis.print_comparison("top_categories-themes")
    analysis.print_comparison()

    analysis_2 = EmbeddingAnalysis(
        api_key=openai_api_key,
        file_name="inaccurate_similarity_results.txt",
        plt_prefix="analysis_2_",
        save_dir="Plots/Analysis_2",
    )

    # Store multiple strings and lists
    analysis_2.embed_strings(
        top_categories=[
            "Social and Information Sciences",
            "Mathematics",
            "Quantitative Biology",
        ],
        mid_categories=[
            "Human-Computer Interaction",
            "Computation and Language, Computational Complexity",
            "Quantitative Methods",
        ],
        themes=[
            "Expertise Utilization",
            "Team Processes",
            "Intragroup Conflicts",
            "Perceived Expertise",
            "Social Status",
            "Influence Relationships",
        ],
        title=[
            "The Effects of Expertise and Social Status on Team Member Influence and the Moderating Roles of Intragroup Conflicts"
        ],
        abstract=[
            "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice."
        ],
    )

    # Print all strings and similarities
    print(analysis_2)

    analysis_2.print_comparison()

    analysis_3 = EmbeddingAnalysis(
        api_key=openai_api_key,
        file_name="inaccurate_similarity_results_2.txt",
        plt_prefix="analysis_3_",
        save_dir="Plots/Analysis_3",
    )

    analysis_3.embed_strings(
        top_categories=[
            "Economics",
            "Business",
        ],
        mid_categories=[
            "Corporate Finance",
            "International Business",
            "Industrial Organization",
        ],
        themes=[
            "Foreign Equity Ownership",
            "Innovation Investment",
            "R&D Investment",
            "Firm Heterogeneity",
            "Monitoring Mechanisms",
            "Moderation Effects",
        ],
        title=[
            "Changes in foreign ownership and innovation investment: the case of Korean corporate governance reforms"
        ],
        abstract=[
            "The goal of this paper is to investigate how deregulating foreign equity ownership influences a firm's innovation investment. We attempt to answer this question using data from 530 Korean manufacturing firms between 1998 and 2003 through generalised estimating equations. Our findings suggest that foreign ownership and R&D investment exhibit an inverted U-shaped relationship because the incentives to monitor managers' decision-making processes initially play a greater role, but this role stagnates as the share owned by foreign investors becomes concentrated. In addition, we consider firm heterogeneity and observe the negative moderation effects of firm age and the positive moderation effects of growth opportunity."
        ],
    )

    # Print all strings and similarities
    print(analysis_3)

    analysis_3.print_comparison()

    analysis_4 = EmbeddingAnalysis(
        api_key=openai_api_key,
        file_name="inaccurate_similarity_results_3.txt",
        plt_prefix="analysis_4_",
        save_dir="Plots/Analysis_4",
    )

    analysis_4.embed_strings(
        top_categories=["Business and Economics", "Statistics", "Computer Science"],
        mid_categories=[
            "Business Strategy",
            "Data Analysis",
            "Machine Learning",
            "Acquisition Strategies",
        ],
        themes=[
            "Exploration vs. Exploitation",
            "Cluster Analysis",
            "Alliance Patterns",
            "Acquisition Patterns",
        ],
        title=["Patterns of alliances and acquisitions: An exploratory study"],
        abstract=[
            "This study examined how firms combine alliances and acquisitions in an exploration/exploitation framework. By conducting cluster analysis on a sample of 1270 acquisitions made by 836 firms, we first identified the patterns in alliance and acquisition activities undertaken by these firms. Five distinct patterns were identified: (I) low alliance-low acquisition, (II) low alliance-high acquisition, (III) high alliance-low acquisition, (IV) high alliance-high acquisition, and (V) medium alliance-very high acquisition. Next, we analyzed the different ways in which the two modes were interlinked within these five patterns for exploration/exploitation. Patterns III and IV appeared to involve both exploration/exploitation and mutually reinforce exploration/exploitation. In contrast, in the remaining patterns, the two modes appeared to be more loosely coupled with each other, with a focus on exploitation."
        ],
    )

    print(analysis_4)

    analysis_4.print_comparison()
