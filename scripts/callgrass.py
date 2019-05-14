if __name__ == '__main__':

import grass.script as grass
grass.run_command("v.to.db", map='bl@PERMANENT', layer='2', option='start', units='meters', columns='X,Y,Z')

print "Grass OUtput"