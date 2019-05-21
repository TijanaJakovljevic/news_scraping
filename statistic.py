from libs.db.client import connect_to_database
from libs.db.models import Article
import pandas as pd
import numpy as np

from collections import Counter
import matplotlib.pyplot as plt

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def show_data():

    df_blic, df_kurir, tags, tags_blic, tags_kurir, title = prepare_data_for_statistic()

    most_common_titles = Counter(title).most_common()

    tag_frequency_bar(tags)
    tag_frequency_bar(tags_blic)
    tag_frequency_bar(tags_kurir)

    foto_blic = list(df_blic[df_blic.title.str.contains("(FOTO)")]["title"])
    foto_kurir = list(df_kurir[df_kurir.title.str.contains("(FOTO)")]["title"])
    video_blic = list(df_blic[df_blic.title.str.contains("(VIDEO)")]["title"])
    video_kurir = list(df_kurir[df_kurir.title.str.contains("(VIDEO)")]["title"])
    foto_video_blic = list(
        df_blic[df_blic.title.str.contains("(VIDEO)") & df_blic.title.str.contains("(FOTO)")]["title"]
    )
    foto_video_kurir = list(
        df_kurir[df_kurir.title.str.contains("(VIDEO)") & df_kurir.title.str.contains("(FOTO)")]["title"]
    )

    table_for_images(df_blic)
    table_for_images(df_kurir)

    table_for_authors(df_blic)
    table_for_authors(df_kurir)

    table_for_categories(df_blic)
    table_for_categories(df_kurir)

    table_for_comments(df_blic)
    table_for_comments(df_kurir)

    # top_10_comments = df.sort_values(by=["comment_count"], ascending=False).head(10).reset_index()
    # top_10_comments.plot(kind="bar", y="comment_count", use_index=True)
    # plt.title("comment_count")
    # plt.show()

    # bars
    number_of_accurencies_in_title_per_month(df_blic, "Tramp")
    number_of_accurencies_in_title_per_month(df_kurir, "tramp")

    number_of_articles_per_month(df_blic)
    number_of_articles_per_month(df_kurir)
    number_of_articles_per_day(df_blic)
    number_of_articles_per_day(df_kurir)
    number_of_articles_per_weekday(df_blic)
    number_of_articles_per_weekday(df_kurir)
    number_of_articles_per_hour(df_blic)
    number_of_articles_per_hour(df_kurir)
    number_of_articles_per_hour_per_weekday_in_one_figure(df_blic)
    number_of_articles_per_hour_per_weekday_in_one_figure(df_kurir)
    number_of_articles_per_hour_per_weekday_in_separate_figures(df_blic)
    number_of_articles_per_hour_per_weekday_in_separate_figures(df_kurir)


def prepare_data_for_statistic():
    connect_to_database()

    articles = Article.objects(full_article_scraped=True)

    article_list = []
    tags = []
    tags_blic = []
    tags_kurir = []
    title = []
    i = 0
    for article in articles:
        i += 1
        if article.short_description and len(article.short_description) >= 2000:
            article.short_description = article.short_description[:1999]
            article.save()

        if i > 53800:
            article.title = article.title.lower()
            article.save()
            print(f" {i}, {article.title}")
        else:
            print(f" {i}")

        article_list.append(article._data)
        title.append(article.title)
        tags += [tag.strip() for tag in list(article.tags)]
        if "blic.rs" in article.url:
            tags_blic += [tag.strip() for tag in list(article.tags)]
        if "kurir.rs" in article.url:
            tags_kurir += [tag.strip() for tag in list(article.tags)]

    df = pd.DataFrame(article_list)
    df_blic = df[(df["url"].str.contains("blic.rs"))]
    df_kurir = df[(df["url"].str.contains("kurir.rs"))]

    return df_blic, df_kurir, tags, tags_blic, tags_kurir, title


def number_of_accurencies_in_title_per_month(dataframe, param):
    frequncy_per_month = dataframe[dataframe.title.str.contains(param)]
    number_of_articles_by_month = frequncy_per_month.groupby(
        pd.to_datetime(dataframe["article_datetime"]).dt.month
    ).size()
    number_of_articles_by_month = number_of_articles_by_month.reset_index().rename(
        columns={"article_datetime": "month", 0: "article_count"}
    )
    number_of_articles_by_month.plot(x="month", y="article_count")
    plt.title("Number of articles per month with '{}' in it".format(param))
    plt.xticks(np.arange(0, 12, step=1))
    plt.yticks(np.arange(0, 250, step=25))
    plt.show()


def number_of_articles_per_hour(df_blic):
    articles_per_hour = df_blic.groupby(pd.to_datetime(df_blic["article_datetime"]).dt.hour).size()
    articles_per_hour = articles_per_hour.reset_index().rename(columns={"article_datetime": "hour", 0: "article_count"})
    articles_per_hour.plot.bar(x="hour", y="article_count")
    plt.show()


def number_of_articles_per_weekday(df_blic):
    articles_by_weekday = df_blic.groupby(pd.to_datetime(df_blic["article_datetime"]).dt.weekday).size()
    articles_by_weekday = articles_by_weekday.reset_index().rename(
        columns={"article_datetime": "weekday", 0: "article_count"}
    )
    articles_by_weekday.plot.bar(x="weekday", y="article_count")
    plt.show()


def number_of_articles_per_day(df_blic):
    articles_by_day = df_blic.groupby(pd.to_datetime(df_blic["article_datetime"]).dt.day).size()
    articles_by_day = articles_by_day.reset_index().rename(columns={"article_datetime": "day", 0: "article_count"})
    articles_by_day.plot.bar(x="day", y="article_count")
    plt.show()


def number_of_articles_per_month(df_blic):
    number_of_articles_by_month = df_blic.groupby(pd.to_datetime(df_blic["article_datetime"]).dt.month).size()
    number_of_articles_by_month = number_of_articles_by_month.reset_index().rename(
        columns={"article_datetime": "month", 0: "article_count"}
    )
    number_of_articles_by_month.plot.bar(x="month", y="article_count")
    plt.show()


def number_of_articles_per_hour_per_weekday_in_one_figure(df_blic):
    fig, ax = plt.subplots()
    for day in range(0, len(WEEKDAYS)):
        one_weekday_articles = df_blic[pd.to_datetime(df_blic["article_datetime"]).dt.weekday == day]
        articles_per_hour = one_weekday_articles.groupby(pd.to_datetime(df_blic["article_datetime"]).dt.hour).size()
        articles_per_hour = articles_per_hour.reset_index().rename(
            columns={"article_datetime": "hour", 0: "article_count"}
        )
        ax.bar(articles_per_hour.hour, articles_per_hour.article_count, label=WEEKDAYS[day])
    ax.set_ylabel("Scores")
    ax.set_title("Number of articles per hour")
    ax.legend()
    plt.show()


def number_of_articles_per_hour_per_weekday_in_separate_figures(df_blic):
    for day in range(0, len(WEEKDAYS)):
        one_weekday_articles = df_blic[pd.to_datetime(df_blic["article_datetime"]).dt.weekday == day]
        articles_per_hour = one_weekday_articles.groupby(pd.to_datetime(df_blic["article_datetime"]).dt.hour).size()
        articles_per_hour = articles_per_hour.reset_index().rename(
            columns={"article_datetime": "hour", 0: "article_count"}
        )
        plt.bar(articles_per_hour.hour, articles_per_hour.article_count, label=WEEKDAYS[day])
        plt.ylabel("Counts")
        plt.yticks(np.arange(0, 1000, step=100))
        plt.xticks(np.arange(0, 24, step=1))
        plt.title("Number of articles per hour for {}".format(WEEKDAYS[day]))
        plt.legend()
        plt.show()


def table_for_images(df_blic):
    images = df_blic.sort_values(by=["img_number"], ascending=False).head(20)[["img_number", "title"]]
    create_table_from_df(images.values, images.columns)


def tag_frequency_bar(tags):
    tag_frequency = Counter(tags).most_common()
    db_tag_frequency = pd.Series(dict(tag_frequency)).reset_index().rename(columns={0: "Count", "index": "Tag"})
    db_tag_frequency.head(20).sort_values("Count").plot.barh(x="Tag", y="Count")
    plt.title("Kurir")
    plt.xticks(np.arange(0, 5000, step=1000))
    plt.show()


def table_for_categories(df_blic):
    categ = df_blic.groupby(["category", "subcategory"]).size().sort_values(ascending=False).nlargest(20)
    categ = categ.reset_index().rename(columns={0: "count"})
    categ["category / subcategory"] = categ[["category", "subcategory"]].apply(lambda x: " / ".join(x), axis=1)
    categ = categ[["category / subcategory", "count"]]
    create_table_from_df(categ.values, categ.columns)


def table_for_comments(df):
    top_comments = df.sort_values(by=["comment_count"], ascending=False).head(9)[["title", "comment_count"]]
    create_table_from_df(top_comments.values, top_comments.columns)


def table_for_authors(df_blic):
    top_authors = df_blic["author"].value_counts().sort_values(ascending=False).nlargest(10)
    top_authors = top_authors.reset_index().rename(columns={"index": "authors", "author": "count"})

    create_table_from_df(top_authors.values, top_authors.columns)


def create_table_from_df(values, columns):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")
    ax.table(cellText=values, colLabels=columns, cellLoc="center", loc="center", fontsize=10)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    show_data()

    # todo: broj vesti sa preko X komentara
    # todo: broj autora sa preko X naslova

    # todo: najpupularniji tagovi u foto/video vestima
    # todo: broj istih naslova u blicu i kuriru
