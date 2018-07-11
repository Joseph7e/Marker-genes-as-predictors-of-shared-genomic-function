from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
# import sys
#
# str = ''
#
# file = open(sys.argv[1], 'r')
#
# for line in file:
#     str += line.rstrip()# + ","

def generate_cloud(text, out):
    # Generate a word cloud image

    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud)
    plt.axis("off")

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud().generate(text)
    # fig = plt.figure()
    plt.figure(figsize=(10, 5))
    # ax = plt.Axes(fig, [0., 0., 1., 1.])
    # ax.set_axis_off()
    # fig.add_axes(ax)
    fig = plt.imshow(wordcloud)
    plt.axis("off")
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    # plt.show()
    # plt.savefig("/home/genome/airjordan/bin/python_libs/misc/clustering/clouds/" + out + ".png") #, bbox_inches='tight')
    plt.savefig(out + ".png", bbox_inches='tight', pad_inches=0)
    plt.close()

# mycloud.generate_cloud(str,'word_out')
