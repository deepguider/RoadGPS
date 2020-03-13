#ifndef __TEST_SIMPLE_MAP__
#define __TEST_SIMPLE_MAP__

#include "../unit_test/vvs.h"
#include "dg_map_manager.hpp"
#include <stdint.h>
#include <cstdint>

int testSimpleMapManager()
{
	dg::MapManager manager;

    // Load the map
	VVS_CHECK_TRUE(manager.load(36.384063, 127.374733, 650.0));
	VVS_CHECK_EQUL(manager.getMap().nodes.size(), 721); //8856); // 2);
	
	// Generate the path
	manager.generatePath(37.503884, 127.047569, 37.5087, 127.0621);

	// Get the path
	dg::Path path = manager.getPath();
	VVS_CHECK_EQUL(path.pts.size(), 109); // 78);
	path = manager.getPath("test_simple_path.json");
	VVS_CHECK_EQUL(path.pts.size(), 78);
	
	dg::Node* findNode = manager.getMap().findNode(559542564800095);
	VVS_CHECK_EQUL(findNode->id, 559542564800095);
	dg::Edge* findEdge = manager.getMap().findEdge(559562564900154, 559562564900155);
	VVS_CHECK_EQUL(findEdge->length, 13.370689140764002);
	VVS_CHECK_EQUL((manager.getMap().findEdge(findEdge->id))->length, 13.370689140764002);

	VVS_CHECK_EQUL(manager.getPOI(36.384063, 127.374733, 650.0).size(), 613);
	VVS_CHECK_EQUL(manager.getPOI(559542564800095, 500.0).size(), 212);
	//std::vector<cv::Point2d> poiloc = manager.getPOIloc("UST");
	
    return 0;
}

#endif // End of '__TEST_SIMPLE_MAP__'
