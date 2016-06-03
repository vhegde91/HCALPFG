#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
import FWCore.ParameterSet.VarParsing as VarParsing


#------------------------------------------------------------------------------------
# Declare the process and input variables
#------------------------------------------------------------------------------------
#process = cms.Process('NOISE',eras.Run2_50ns)#for 50ns 13 TeV data
process = cms.Process('NOISE',eras.Run2_25ns)#for 25ns 13 TeV data
options = VarParsing.VarParsing ('analysis')
options.register ('skipEvents', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "no of skipped events")
#options.inputFiles = '/store/data/Run2015D/DoubleMuon/RECO/16Dec2015-v1/10000/002C811B-80A7-E511-8C4D-0CC47A4D7644.root'
#options.inputFiles = '/store/data/Commissioning2016/MinimumBias/RECO/PromptReco-v1/000/266/653/00000/14AC0364-52E9-E511-A737-02163E0146FA.root'
#options.inputFiles = 'root://xrootd-cms.infn.it//store/data/Run2016B/NoBPTX/RECO/PromptReco-v1/000/272/147/00000/5484BE2E-8211-E611-9A9F-02163E01476B.root'
#options.inputFiles = 'root://xrootd-cms.infn.it//store/data/Run2016B/JetHT/RECO/PromptReco-v2/000/273/150/00000/CC80E0AF-DA19-E611-BF0D-02163E014456.root'
#options.inputFiles = 'file:Run2016JetHT_273150_50Events.root'
#options.inputFiles = 'root://xrootd.unl.edu///store/data/Run2015D/JetHT/RECO/PromptReco-v4/000/258/159/00000/6269BC62-D16B-E511-A54D-02163E011A36.root'
#options.outputFile = 'results.root'
options.maxEvents = -1 # -1 means all events
#options.skipEvents = 0 # default is 0.


#------------------------------------------------------------------------------------
# Get and parse the command line arguments
#------------------------------------------------------------------------------------
options.parseArguments()
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.source = cms.Source("PoolSource",
    fileNames  = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents) # default is 0.
)

process.TFileService = cms.Service("TFileService",
      fileName = cms.string('HF2016B_Run273158to273450.root')
#     fileName = cms.string(options.outputFile)
)


#------------------------------------------------------------------------------------
# import of standard configurations
#------------------------------------------------------------------------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#vvvprocess.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')


#------------------------------------------------------------------------------------
# Set up L1 Jet digis #Disabled 
#------------------------------------------------------------------------------------
#process.load("HCALPFG.HcalTupleMaker.HcalL1JetDigisProducer_cfi")


#------------------------------------------------------------------------------------
# Set up our analyzer
#------------------------------------------------------------------------------------
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_cfi") # Dont want to use this, load modules individually
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Tree_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Event_cfi")
#vvvprocess.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHEDigis_cfi")
#vvvprocess.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHERecHits_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HFRecHits_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Trigger_cfi")


#------------------------------------------------------------------------------------
# Set up noise filters
#------------------------------------------------------------------------------------
#vvvprocess.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalNoiseFilters_cfi") # This is over-ridden below to remove Method0-Method2 dual reco.
#------------------------------------------------------------------------------------
# Set up iso noise filter parameters, used for iso-noise filter study in 25ns.
#------------------------------------------------------------------------------------
#vvvprocess.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalIsoNoiseFilterParameters_cfi")
#------------------------------------------------------------------------------------
# Set up CaloJetMet quantities 
#------------------------------------------------------------------------------------
#vvvprocess.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_CaloJetMet_cfi") # This is over-ridden below to remove Method0-Method2 dual reco.
#------------------------------------------------------------------------------------
# Set up MuonTrack quantities 
#------------------------------------------------------------------------------------
#vvvprocess.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_MuonTrack_cfi")


#------------------------------------------------------------------------------------
# Specify Global Tag
#------------------------------------------------------------------------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v4'
#process.GlobalTag.globaltag = '76X_dataRun2_v16'
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['run2_data']


############################################# Changes made by vinay for filtering events based on triggers ##########################################
#------------------------------------------------------------------------------------
# Disabled since we dont deal with HLT
#------------------------------------------------------------------------------------
process.my_hlt = cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
#     HLTPaths = cms.vstring("HLT_L1SingleJet16*"), # provide list of HLT paths (or patterns) you want
                              HLTPaths = cms.vstring("HLT_CaloJet500_NoJetID_*",
                                                     "HLT_DiPFJetAve500_*",
                                                     "HLT_PFHT750_4JetPt50_*",
                                                     "HLT_PFHT800_*",
                                                     "HLT_PFJet450_*"),
    eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
    andOr = cms.bool(True),             # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
    throw = cms.bool(False)    # throw exception on unknown path names
)
############################################# Changes made by vinay end here ##### (by default all these were commneted ############################# 

#------------------------------------------------------------------------------------
#Remove Method 0, Rename Method 2 as "default" where necessary:
#------------------------------------------------------------------------------------
process.hcalTupleCaloJetMet = cms.EDProducer("HcalTupleMaker_CaloJetMet",
         recoInputTag         = cms.untracked.string("hbhereco"),
         Prefix = cms.untracked.string(""),
         Suffix = cms.untracked.string("")
)
process.hcalTupleHcalNoiseFilters = cms.EDProducer("HcalTupleMaker_HcalNoiseFilters",
         noiseSummaryInputTag = cms.untracked.InputTag("hcalnoise"),
         noiseResultInputTag  = cms.untracked.string("HBHENoiseFilterResultProducer"),
         recoInputTag         = cms.untracked.string("hbhereco"),
         isRAW  = cms.untracked.bool(False), # new Flag necessary for HcalNoiseFilters to run on RECO data
         isRECO = cms.untracked.bool(True), 
         Prefix = cms.untracked.string(""),
         Suffix = cms.untracked.string("")
)


#------------------------------------------------------------------------------------
# Place-holder for applying HBHE noise filter:
#------------------------------------------------------------------------------------
#process.ApplyBaselineHBHENoiseFilter = cms.EDFilter('BooleanFlagFilter',
#    inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),    
#    #inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun1'),
#    #inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Loose'),
#    #inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Tight'),
#    reverseDecision = cms.bool(False)
#)


#------------------------------------------------------------------------------------
# This enables NEF flagging, but needs reconstruction of RAW data.
# This is not needed for datasets reconstructed with >=CMSSW748:
# i.e. 2015C Prompt-reco has NEF flags computed out-of-the-box.
#------------------------------------------------------------------------------------
#process.hbheprereco.setNegativeFlags          = cms.bool(True)

process.goodOfflinePrimaryVertices = cms.EDFilter("VertexSelector",
#process.VertexCollection = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof >= 4.0 && abs(z) <= 24.0 && abs(position.Rho) <= 2.0"),
    filter = cms.bool(False)
)

#------------------------------------------------------------------------------------
# HcalTupleMaker sequence definition
#------------------------------------------------------------------------------------
process.tuple_step = cms.Sequence(
#    process.VertexCollection*
    process.goodOfflinePrimaryVertices*
    # Make HCAL tuples: Event, run, ls number
    process.hcalTupleEvent*
    # Make HCAL tuples: FED info
    #    process.hcalTupleFEDs*
    #    # Make HCAL tuples: digi info
    #raw# process.hcalTupleHBHEDigis*
    #    process.hcalTupleHODigis*
    #    process.hcalTupleHFDigis*
    #    process.hcalTupleTriggerPrimitives*
    #    # Make HCAL tuples: digi info
    #    process.hcalTupleHBHECosmicsDigis*
    #    process.hcalTupleHOCosmicsDigis*
    #    # Make HCAL tuples: digi info
    #    process.hcalTupleHBHEL1JetsDigis*
    #    process.hcalTupleHFL1JetsDigis*
    #    process.hcalTupleL1JetTriggerPrimitives*
    #    # Make HCAL tuples: reco info
#vvv    process.hcalTupleHBHERecHits*
    process.hcalTupleHFRecHits*
#vvv    process.hcalTupleHcalNoiseFilters*
#vvv    process.hcalTupleHcalIsoNoiseFilterParameters* #for studying iso-noise-filter
#vvv    process.hcalTupleCaloJetMet*
#vvv    process.hcalTupleMuonTrack*
    #
    #process.hcalTupleHBHERecHitsMethod0*
    #process.hcalTupleHcalNoiseFiltersMethod0*
    #process.hcalTupleCaloJetMetMethod0*
    #    process.hcalTupleHORecHits*
    #    process.hcalTupleHFRecHits*
    #    # Trigger info
    process.hcalTupleTrigger*
    
    #    process.hcalTupleTriggerObjects*
    #    # L1 jet info
    #    process.hcalTupleL1Jets*
    #    # Make HCAL tuples: cosmic muon info
    #    process.hcalTupleCosmicMuons*
    #    # Package everything into a tree
    #
    process.hcalTupleTree
)


#-----------------------------------------------------------------------------------
# Path and EndPath definitions
#-----------------------------------------------------------------------------------
process.preparation = cms.Path(
#    process.my_hlt *
    #process.RawToDigi * #needed for RAW files
    #process.L1Reco *
    #rprocess.reconstruction * #needed for RAW files
    #process.caloglobalreco *
    #process.reconstructionCosmics *
    #
    #process.horeco *
    #process.hfreco *
    #
    #process.hbheprerecoMethod0 *
    #process.hbheprerecoMethod2 *
    #process.hbherecoMethod0 *
    #process.hbherecoMethod2 *
    #
    #process.towerMakerMethod0 *
    #process.towerMakerMethod2 *
    #
    #process.hcalnoiseMethod0 *
    #process.hcalnoiseMethod2 *
    #
    #process.HBHENoiseFilterResultProducerMethod0 *
    #process.HBHENoiseFilterResultProducerMethod2 *
    #
    #
    #process.hcalCosmicDigis *
    #process.hcalL1JetDigis *
    #
    #process.hcalnoise *  #needed for RAW files
#vvv    process.HBHENoiseFilterResultProducer *
    #process.ApplyBaselineHBHENoiseFilter *
    #
    process.tuple_step
)
