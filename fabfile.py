from fabric.api import env, run, roles, put, get
env.hosts = [
    # "slice320.pcvm3-1.geni.case.edu",
 #   "slice320.pcvm1-1.geni.it.cornell.edu",
    "192.168.22.144",
    # "slice320.pcvm2-2.instageni.rnoc.gatech.edu",
    # "slice320.pcvm3-2.instageni.illinois.edu",
    # "slice320.pcvm5-7.lan.sdn.uky.edu",
    # "slice320.pcvm3-1.instageni.lsu.edu",
    # "slice320.pcvm2-2.instageni.maxgigapop.net",
  #   "slice320.pcvm1-1.instageni.iu.edu",
  #   "slice320.pcvm3-4.instageni.rnet.missouri.edu",
  #   "slice320.pcvm3-7.instageni.nps.edu",
  #   "slice320.pcvm2-1.instageni.nysernet.org",
  #   "slice320.pcvm3-11.genirack.nyu.edu",
  #   "slice320.pcvm5-1.instageni.northwestern.edu",
  #   "slice320.pcvm5-2.instageni.cs.princeton.edu",
  #   "slice320.pcvm3-3.instageni.rutgers.edu",
  #   "slice320.pcvm1-6.instageni.sox.net",
  #   "slice320.pcvm3-1.instageni.stanford.edu",
  #   "slice320.pcvm2-1.instageni.idre.ucla.edu",
  #   "slice320.pcvm4-1.utahddc.geniracks.net",
  #   "slice320.pcvm1-1.instageni.wisc.edu",
  
  ]

env.key_filename="id_rsa"
env.use_ssh_config = True
env.ssh_config_path = 'ssh-config'

env.roledefs.update({
  'replica': ['192.168.22.144', 'localhost'],
  'remote':['192.168.22.144']
  })


def uptime():
    run('uptime')

@roles('replica')
def hello():
  run('echo hello')

@roles('remote')
def putFile():
  put('replica.py', './dis')

