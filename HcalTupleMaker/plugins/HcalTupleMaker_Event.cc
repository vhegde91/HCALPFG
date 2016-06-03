#include "HCALPFG/HcalTupleMaker/interface/HcalTupleMaker_Event.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/EventBase.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/EDGetToken.h"

HcalTupleMaker_Event::HcalTupleMaker_Event(const edm::ParameterSet& iConfig)
{
  produces <unsigned int> ( "nPrimaryVertices"    );
  produces <unsigned int> ( "run"    );
  produces <unsigned int> ( "event"  );
  produces <unsigned int> ( "ls"     );
  produces <unsigned int> ( "bx"     );
  vertexCollectionTok_ =  consumes<reco::VertexCollection>(edm::InputTag("offlinePrimaryVertices"));
}

void HcalTupleMaker_Event::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  //  edm::Handle<reco::VertexCollection> vtx;
  //  bool gotVtx = iEvent.getByLabel("goodOfflinePrimaryVertices", vtx);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vertexCollectionTok_,vertices);
  bool gotVtx=false;

  if( vertices.isValid() ) gotVtx=true;
  if (!gotVtx ) {
    std::cout << "goodOfflinePrimaryVertices not found " << std::endl;
    return;
  }

  std::auto_ptr<unsigned int >  nPrimaryVertices   ( new unsigned int(vertices->size()  ) );
  std::auto_ptr<unsigned int >  run   ( new unsigned int(iEvent.id().run()        ) );
  std::auto_ptr<unsigned int >  event ( new unsigned int(iEvent.id().event()      ) );
  std::auto_ptr<unsigned int >  ls    ( new unsigned int(iEvent.luminosityBlock() ) );

  edm::EventBase const & eventbase = iEvent;
  std::auto_ptr<unsigned int >  bx    ( new unsigned int(eventbase.bunchCrossing() ) );
  
  iEvent.put( nPrimaryVertices,  "nPrimaryVertices"   );
  iEvent.put( run,   "run"   );
  iEvent.put( event, "event" );
  iEvent.put( ls   , "ls"    );
  iEvent.put( bx   , "bx"    );

}
