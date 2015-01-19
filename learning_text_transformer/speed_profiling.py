"""Time .apply on each Transform operation"""
import timeit
import transforms

if __name__ == "__main__":
    nbr_iterations = 10000
    input_string = "this is an input string sóciété"
    output_string = ""
    #input_string = "SchÃ¶n"
    #output_string = "schön"
    list_of_transforms = transforms.get_transforms([input_string], [output_string])

    results = []
    for n, transform in enumerate(list_of_transforms):
        transform.apply(input_string)
        setup = "import transforms; transform = transforms.get_transforms('{inp}', '{out}')[{n}]".format(n=n, inp=input_string, out=output_string)
        timed_result = min(timeit.repeat(stmt="transform.apply('{inp}')".format(inp=input_string), setup=setup, number=nbr_iterations))
        results.append((str(transform), timed_result))

    results.sort(key=lambda x: x[1])
    print("Time cost (s) per {} iterations".format(nbr_iterations))
    for transform, timed_result in results:
        print("{: 2.4f} {}".format(timed_result, transform))

# Worst offender 20150119 (now solved):
# 0.3726 TransformExtractNumber()
#

# Result on 30122014
#Time cost (s) per 10000 iterations
 #0.0047 TransformExpandK
 #0.0047 TransformRemoveDot00
 #0.0053 TransformRemoveWords('Limited')
 #0.0054 TransformRemoveWords('Ltd')
 #0.0072 TransformLowercase
 #0.0670 TransformStrip
 #0.1264 TransformSpokenWordsToNumbers
 #0.1689 TransformUnidecode
 #0.3640 TransformExtractNumber
 #1.4135 TransformFTFY

