# import os
# import psycopg2
# from dotenv import load_dotenv
# import matplotlib.pyplot as plt
# import seaborn as sns
# import sklearn.cluster as cluster
# import matplotlib.ticker as mticker
# import numpy as np

# load_dotenv()


# def elbow_method(cur):
#     command_retrive_data = """
#                 SELECT user_id, COUNT(*) AS purchases
#                 FROM customers
#                 WHERE event_type = 'purchase'
#                 GROUP BY user_id
#                 HAVING COUNT(*) < 25
#                 ORDER BY purchases
#             """

#     cur.execute(command_retrive_data)
#     data = cur.fetchall()
#     data = np.array([x[1] for x in data]).reshape(-1, 1)

#     kmeans_kwargs = {
#         "init": "random",
#         "n_init": 10,
#         "random_state": 1,
#     }

#     K = range(1, 11)
#     wss = []
#     for k in K:
#         kmeans = cluster.KMeans(n_clusters=k, **kmeans_kwargs).fit(data)
#         wss.append(kmeans.inertia_)

#     sns.set(style="darkgrid")
#     fig, ax = plt.subplots()

#     ax.plot(K, wss)
#     ax.set_xlabel('Number of Clusters')
#     ax.set_xlim(0, 11)
#     ax.set_title("The Elbow Method")

#     # Remove Scientific Notation
#     ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=False))
#     ax.ticklabel_format(style='plain', axis='y')
#     plt.show()


# def call_data():
#     conn = psycopg2.connect(
#         user=os.getenv('POSTGRES_LOGIN'),
#         password=os.getenv('POSTGRES_PASSWORD'),
#         host="localhost",
#         port="5432",
#         database=os.getenv('POSTGRES_NAME')
#     )
#     cur = conn.cursor()

#     elbow_method(cur)

#     conn.commit()
#     cur.close()
#     conn.close()


# def main():
#     try:
#         call_data()
#     except AssertionError as error:
#         print(AssertionError.__name__ + ":", error)


# if __name__ == "__main__":
#     main()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

# Génération de données fictives
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# Initialisation aléatoire des centroïdes
def init_centroids(X, k):
    indices = np.random.choice(X.shape[0], k, replace=False)
    return X[indices]

def plot_kmeans_step(X, centroids, labels, title, ax):
    ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', s=30)
    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.5, marker='X')
    ax.set_title(title)

def assign_labels(X, centroids):
    # Distance euclidienne entre chaque point et chaque centroïde
    distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)

def move_centroids(X, labels, k):
    return np.array([X[labels == i].mean(axis=0) for i in range(k)])

# Paramètres
k = 4
centroids = init_centroids(X, k)
fig, axs = plt.subplots(1, 4, figsize=(18, 4))

# Etape 1 : Initialisation
labels = assign_labels(X, centroids)
plot_kmeans_step(X, centroids, labels, "Initialisation", axs[0])

# Etape 2 : Première affectation
centroids = move_centroids(X, labels, k)
labels = assign_labels(X, centroids)
plot_kmeans_step(X, centroids, labels, "1ère itération", axs[1])

# Etape 3 : Deuxième itération
centroids = move_centroids(X, labels, k)
labels = assign_labels(X, centroids)
plot_kmeans_step(X, centroids, labels, "2ème itération", axs[2])

# Etape 4 : Résultat final
centroids = move_centroids(X, labels, k)
labels = assign_labels(X, centroids)
plot_kmeans_step(X, centroids, labels, "Clustering final", axs[3])

plt.tight_layout()
plt.show()

