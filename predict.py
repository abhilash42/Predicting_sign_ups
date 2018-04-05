
# coding: utf-8
import treepredict

def main():
    print("Give the details of user:")
    ref=input("Who was your referrer(Slashdot,Google or someone else:)")
    faq=input("Did you read faqs?:")
    pages=int(input("How many pages did you visit:"))
    location=input("Enter your location:")
    list=[ref,location,faq,pages]
    treepredict.classify(list)

if __name__ == '__main__':
    main()

