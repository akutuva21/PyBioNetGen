with open("bionetgen/atomizer/merging/namingDatabase.py", "r") as f:
    content = f.read()

content = content.replace(
    'queryStatement = "SELECT annotationURI,annotationName from moleculeNames as M join identifier as I ON M.ROWID == I.speciesID join annotation as A on A.ROWID == I.annotationID and M.name == ?"',
    "queryStatement = 'SELECT annotationURI,annotationName from moleculeNames as M join identifier as I ON M.ROWID == I.speciesID join annotation as A on A.ROWID == I.annotationID and M.name == ?'"
)

content = content.replace(
    'queryStatement = "SELECT B.file,M.name from moleculeNames as M join biomodels as B on B.ROWID == M.fileID WHERE M.name == ?"',
    "queryStatement = 'SELECT B.file,M.name from moleculeNames as M join biomodels as B on B.ROWID == M.fileID WHERE M.name == ?'"
)

content = content.replace(
    'queryStatement = "SELECT B.file,A.annotationName from biomodels as B join annotation as A on B.organismID == A.ROWID WHERE A.annotationName == ?"',
    "queryStatement = 'SELECT B.file,A.annotationName from biomodels as B join annotation as A on B.organismID == A.ROWID WHERE A.annotationName == ?'"
)

content = content.replace(
    'queryStatement = "SELECT name,A.annotationURI from moleculeNames as M join identifier as I ON M.ROWID == I.speciesID join annotation as A on A.ROWID == I.annotationID and A.annotationURI == ?"',
    "queryStatement = 'SELECT name,A.annotationURI from moleculeNames as M join identifier as I ON M.ROWID == I.speciesID join annotation as A on A.ROWID == I.annotationID and A.annotationURI == ?'"
)

content = content.replace(
    'queryStatement = "SELECT B.file,name,A.annotationURI,A.annotationName,qualifier from moleculeNames as M join identifier as I ON M.ROWID == I.speciesID \\\n                            join annotation as A on A.ROWID == I.annotationID join biomodels as B on B.ROWID == M.fileID and B.file == ?"',
    "queryStatement = 'SELECT B.file,name,A.annotationURI,A.annotationName,qualifier from moleculeNames as M join identifier as I ON M.ROWID == I.speciesID \\\n                            join annotation as A on A.ROWID == I.annotationID join biomodels as B on B.ROWID == M.fileID and B.file == ?'"
)

content = content.replace(
    'queryStatement = "select file from biomodels WHERE file == ?"',
    "queryStatement = 'select file from biomodels WHERE file == ?'"
)

content = content.replace(
    '''    cursor.execute(
        "select ROWID from annotation WHERE annotationURI == ?",
        (annotationNames[-1][0],),
    )''',
    '''    cursor.execute(
        'select ROWID from annotation WHERE annotationURI == ?',
        (annotationNames[-1][0],)
    )'''
)

content = content.replace(
    'cursor.execute("select ROWID from biomodels WHERE file == ?", (fileName2,))',
    "cursor.execute('select ROWID from biomodels WHERE file == ?', (fileName2,))"
)

content = content.replace(
    '''    moleculeIDs = {
        x[1]: x[0]
        for x in cursor.execute(
            "select ROWID,name from moleculeNames WHERE moleculeNames.fileId == ?",
            (modelID,),
        )
    }''',
    '''    moleculeIDs = {
        x[1]: x[0]
        for x in cursor.execute(
            "select ROWID,name from moleculeNames WHERE moleculeNames.fileId == ?",
            (modelID,)
        )
    }'''
)

with open("bionetgen/atomizer/merging/namingDatabase.py", "w") as f:
    f.write(content)
