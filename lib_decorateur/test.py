from GenericTools import chronometre

"decorateur qui trace le chronometage d une methode de specifiee"
@chronometre
def test():
    print('ok')

test()