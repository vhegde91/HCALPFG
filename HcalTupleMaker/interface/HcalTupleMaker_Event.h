#ifndef HcalTupleMaker_Event_h
#define HcalTupleMaker_Event_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/EDGetToken.h"


class HcalTupleMaker_Event : public edm::EDProducer {
 public:
  explicit HcalTupleMaker_Event(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  //  edm::InputTag vertexCollectionTag_;
  edm::EDGetTokenT<reco::VertexCollection> vertexCollectionTok_;
};

#endif
