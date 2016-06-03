from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'HF2016B_Run_273158to273450'
config.General.workArea = 'crab_projectRun_273158to273450'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'noiseAnalysis_CollisionData_RECO_cfg.py'

config.Data.inputDataset = '/JetHT/Run2016B-PromptReco-v2/RECO'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 25
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/Cert_271036-273450_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
config.Data.runRange = '273158-273450'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'CRAB3_HF2016B_273158to273450'

config.Site.storageSite = 'T2_IN_TIFR'
