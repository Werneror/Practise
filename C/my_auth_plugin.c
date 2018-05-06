/* Copyright (C) 2018 Werner */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <mysql/plugin_auth.h>
#include <mysql/auth_dialog_client.h>

static int school_number_auth(MYSQL_PLUGIN_VIO *vio, MYSQL_SERVER_AUTH_INFO *info)
{
    int pkt_len;
    unsigned char *pkt;

    if (vio->write_packet(vio, (const unsigned char *) ORDINARY_QUESTION "Please enter your name: ", 26))
        return CR_ERROR;

    if ((pkt_len= vio->read_packet(vio, &pkt)) < 0)
        return CR_ERROR;

    if (strcmp((const char *) pkt, info->user_name))
        return CR_ERROR;

    if (vio->write_packet(vio, (const unsigned char *) LAST_QUESTION "Please enter your school number: ", 35))
        return CR_ERROR;

    if ((pkt_len= vio->read_packet(vio, &pkt)) < 0)
        return CR_ERROR;

    if (strcmp((const char *) pkt, info->auth_string))
        return CR_ERROR;

    return CR_OK;
}

static struct st_mysql_auth my_auth_plugin=
{
    MYSQL_AUTHENTICATION_INTERFACE_VERSION,
    "dialog",
    school_number_auth
};

mysql_declare_plugin(dialog)
{
    MYSQL_AUTHENTICATION_PLUGIN,
        &my_auth_plugin,
        "school_number",
        "Werner",
        "A simple MariaDB auth plugin",
        PLUGIN_LICENSE_GPL,
        NULL,
        NULL,
        0x0100,
        NULL,
        NULL,
        NULL,
        0,
}
mysql_declare_plugin_end;

