INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_BITCOIN bitcoin)

FIND_PATH(
    BITCOIN_INCLUDE_DIRS
    NAMES bitcoin/api.h
    HINTS $ENV{BITCOIN_DIR}/include
        ${PC_BITCOIN_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    BITCOIN_LIBRARIES
    NAMES gnuradio-bitcoin
    HINTS $ENV{BITCOIN_DIR}/lib
        ${PC_BITCOIN_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(BITCOIN DEFAULT_MSG BITCOIN_LIBRARIES BITCOIN_INCLUDE_DIRS)
MARK_AS_ADVANCED(BITCOIN_LIBRARIES BITCOIN_INCLUDE_DIRS)

