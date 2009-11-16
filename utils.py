def permute(items):
    print 'permute('+ str(items) + ')'
    permutations = []
    if len(items) == 1:
        print 'only one item'
        return [items]
    for item in items:
        remainder = items[:]
        remainder.remove(item)
        for permute_rest in permute(remainder):
            permutation = [item]
            permutation.extend(permute_rest)
            permutations.append(permutation)
    print 'returning ' + str(permutations)
    return permutations

def permute_string(string):
    items = [char for char in string]
    permutations = permute(items)
    strings = [''.join(char) for char in string for string in strings]
    return strings

def main():
    pass

if __name__ == '__main__':
    main()

