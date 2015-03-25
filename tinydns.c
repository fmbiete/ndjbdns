/*
 * tinydns.c: This file is part of the `djbdns' project, originally written
 * by Dr. D J Bernstein and later released under public-domain since late
 * December 2007 (http://cr.yp.to/distributors.html).
 *
 * Copyright (C) 2009 - 2014 Prasad J Pandit
 *
 * This program is a free software; you can redistribute it and/or modify
 * it under the terms of GNU General Public License as published by Free
 * Software Foundation; either version 2 of the license or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * of FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to Free Software Foundation, Inc., 51
 * Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include <unistd.h>

#include "dns.h"
#include "common.h"

#define PIDFILE "/var/run/tinydns.pid"
#define LOGFILE "/var/log/tinydns.log"
#define CFGFILE SYSCONFDIR"/ndjbdns/tinydns.conf"

extern short mode;
extern char pidfile[4096];
extern char logfile[4096];
extern char cfgfile[4096];
static char seed[128];
extern char *cfgfile, *logfile, *pidfile;

void
initialize (void)
{
    cfgfile = cfgfile ? cfgfile : CFGFILE;
    logfile = logfile ? logfile : LOGFILE;
    pidfile = pidfile ? pidfile : PIDFILE;

    read_conf (cfgfile);
    if (mode & DAEMON)
    {
        /* redirect stdout & stderr to a log file */
        redirect_to_log (logfile, STDOUT_FILENO | STDERR_FILENO);
        write_pid (pidfile);
    }

    dns_random_init (seed);
}
